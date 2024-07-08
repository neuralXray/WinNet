
#include "macros.h"
#include "mkl_spblas.f90"
#include "mkl_sparse_qr.f90"
module xtfc_module
    use global_class,    only: net_size
    use parameter_class, only: n_neurons, n_x, w_i, w_f, x_i, x_f

    implicit none

    real(r_kind), dimension(:,:), allocatable :: g
    real(r_kind), dimension(:,:), allocatable :: gd
    real(r_kind), dimension(:,:), allocatable :: jacobian
    real(r_kind), dimension(:),   allocatable :: jacobian_sparse
    integer,      dimension(:),   allocatable :: sparse_rows
    integer,      dimension(:),   allocatable :: sparse_columns
    integer                                   :: nn


    public :: &
        g, gd
    public :: &
       init_xtfc_solver, jacobi_xtfc, jacobi_xtfc_sparse, &
       least_squares, least_squares_sparse, open_file, save_network_beta

    private :: &
        jacobian, jacobian_sparse, sparse_columns, sparse_rows
    private :: &
        save_network_weight



contains

    subroutine init_xtfc_solver()
        use error_msg_class,  only: raise_exception
        use parameter_class,  only: save_network
        implicit none

        real(r_kind) :: g0(n_neurons)
        real(r_kind) :: weight(n_neurons)
        real(r_kind) :: bias(n_neurons)
        real(r_kind) :: x
        real(r_kind) :: i
        integer      :: j
        integer      :: alloc_stat  !< Allocation state


        allocate(g(n_x, n_neurons),  stat=alloc_stat)
        if (alloc_stat .ne. 0) call raise_exception('Allocating "g" failed.', &
                                                    'prepare_simulation', 470001)
        allocate(gd(n_x, n_neurons), stat=alloc_stat)
        if (alloc_stat .ne. 0) call raise_exception('Allocating "gd" failed.', &
                                                    'prepare_simulation', 470001)

        call random_seed()
        call random_number(weight)
        call random_number(bias)
        weight = w_i + (w_f - w_i) * weight
        bias = w_i + (w_f - w_i) * bias

        g0 = tanh(bias)
        g(1, :) = 0
        gd(1, :) = (1 - tanh(bias)**2) * weight
        do i = 2, n_x
            x = x_i + (i - 1) * (x_f - x_i) / (n_x - 1)
            !x = x_i + (x_f - x_i) / 2 ** (n_x - i)
            !x = x_f - (x_f - x_i) / 2 ** (i - 1)
            g(i, :) = tanh(x * weight + bias) - g0
            gd(i, :) = (1 - tanh(x * weight + bias)**2) * weight
        end do

        if (save_network) call save_network_weight(bias, weight)

        write(*,*) "init_xtfc"
    end subroutine init_xtfc_solver



    subroutine jacobi_xtfc(Yi, ydoti, c)
        use single_zone_vars, only: time,T9,rhob,Rkm,Y_p,stepsize,evolution_mode,f
        use jacobian_class,   only: jacobi_init
        use pardiso_class,    only: vals,pt_b,rows
        use error_msg_class,  only: raise_exception
        implicit none

        real(r_kind), intent(in)    :: Yi(n_x, net_size)
        real(r_kind), intent(inout) :: ydoti(n_x, net_size)
        real(r_kind), intent(in)    :: c
        integer      :: i, j, l, m
        integer      :: alloc_stat  !< Allocation state

        if (allocated(jacobian)) deallocate(jacobian)
        allocate(jacobian(n_x * net_size ,  n_neurons * net_size), stat=alloc_stat)
        if (alloc_stat .ne. 0) call raise_exception('Allocating "jacobian" failed.', &
                                                    'prepare_simulation', 470001)

        jacobian = 0
        do i = 1, n_x
            call jacobi_init(time, T9, rhob, Rkm, Yi(i, :), Y_p, ydoti(i, :), &
                             f, stepsize, evolution_mode)
            m = 0
            do l = 1, size(rows)
                if (pt_b(m + 1) .eq. l) then
                    m = m + 1
                end if
                if (m .eq. rows(l)) then
                    jacobian(i + (m - 1)*n_x, 1 + (rows(l) - 1)*n_neurons:rows(l)*n_neurons) = &
                    c * gd(i, :) + g(i, :) * vals(l)
                else
                    jacobian(i + (m - 1)*n_x, 1 + (rows(l) - 1)*n_neurons:rows(l)*n_neurons) = &
                    g(i, :) * vals(l)
                end if
            end do
        end do

    end subroutine jacobi_xtfc



    subroutine jacobi_xtfc_sparse(Yi, ydoti, c)
        use single_zone_vars, only: time,T9,rhob,Rkm,Y_p,stepsize,evolution_mode,f
        use jacobian_class,   only: jacobi_init
        use pardiso_class,    only: vals,pt_b,rows
        use error_msg_class,  only: raise_exception
        implicit none

        real(r_kind), intent(in)    :: Yi(n_x, net_size)
        real(r_kind), intent(inout) :: ydoti(n_x, net_size)
        real(r_kind), intent(in)    :: c
        real(r_kind) :: jacobian(n_x * net_size  *  n_neurons * net_size)
        integer      :: jacobian_rows(n_x * net_size  *  n_neurons * net_size)
        integer      :: jacobian_columns(n_x * net_size  *  n_neurons * net_size)
        integer      :: i, j, l, m, n
        integer      :: alloc_stat  !< Allocation state

        nn = 0
        do i = 1, n_x
            call jacobi_init(time, T9, rhob, Rkm, Yi(i, :), Y_p, ydoti(i, :), &
                             f, stepsize,evolution_mode)
            m = 0
            do l = 1, size(rows)
                if (pt_b(m + 1) .eq. l) then
                    m = m + 1
                end if
                do n = 1, n_neurons
                    if ((gd(i, n) .ne. 0) .and. (m .eq. rows(l))) then
                        nn = nn + 1
                        jacobian(nn) = c * gd(i, n) + g(i, n) * vals(l)
                        jacobian_rows(nn) = i + (m - 1) * n_x
                        jacobian_columns(nn) = n + (rows(l) - 1) * n_neurons
                    else if ((g(i, n) .ne. 0) .and. (vals(l) .ne. 0)) then
                        nn = nn + 1
                        jacobian(nn) = g(i, n) * vals(l)
                        jacobian_rows(nn) = i + (m - 1) * n_x
                        jacobian_columns(nn) = n + (rows(l) - 1) * n_neurons
                    end if
                end do
            end do
        end do

        if (allocated(jacobian_sparse)) deallocate(jacobian_sparse)
        allocate(jacobian_sparse(nn), stat=alloc_stat)
        if (alloc_stat .ne. 0) call raise_exception('Allocating "jacobian_sparse" failed.', &
                                                    'prepare_simulation', 470001)
        if (allocated(sparse_rows)) deallocate(sparse_rows)
        allocate(sparse_rows(nn), stat=alloc_stat)
        if (alloc_stat .ne. 0) call raise_exception('Allocating "sparse_rows" failed.', &
                                                    'prepare_simulation', 470001)
        if (allocated(sparse_columns)) deallocate(sparse_columns)
        allocate(sparse_columns(nn), stat=alloc_stat)
        if (alloc_stat .ne. 0) call raise_exception('Allocating "sparse_columns" failed.', &
                                                    'prepare_simulation', 470001)

        jacobian_sparse = jacobian(1:nn)
        sparse_columns = jacobian_columns(1:nn)
        sparse_rows = jacobian_rows(1:nn)

    end subroutine jacobi_xtfc_sparse



    subroutine least_squares(Loss, beta)
        implicit none

        real(r_kind), intent(in)    :: Loss(n_x * net_size)
        real(r_kind), intent(inout) :: beta(n_neurons, net_size)
        real(r_kind)                :: dbeta(n_neurons, net_size)

        integer :: jpvt(n_neurons * net_size)
        integer :: rank
        integer :: info
        integer :: lwork
        real(r_kind), dimension(:), allocatable :: work


        lwork = 1
        allocate(work(lwork))
        lwork = -1
        jpvt = 0
        call dgelsy(n_x * net_size, n_neurons * net_size, 1, jacobian, n_x * net_size, &
                    Loss, n_x * net_size, jpvt, 1d-12, rank, work, lwork, info)
        lwork = int(work(1))  ! 1082
        deallocate(work)
        allocate(work(lwork))
        jpvt = 0
        call dgelsy(n_x * net_size, n_neurons * net_size, 1, jacobian, n_x * net_size, &
                    Loss, n_x * net_size, jpvt, 1d-12, rank, work, lwork, info)
        deallocate(work)

        beta = beta - reshape(Loss, [n_neurons, net_size])

    end subroutine least_squares



    subroutine least_squares_sparse(Loss, beta)
        use mkl_spblas,    only: SPARSE_INDEX_BASE_ONE, SPARSE_OPERATION_NON_TRANSPOSE, &
                                 SPARSE_LAYOUT_COLUMN_MAJOR, SPARSE_MATRIX_T, &
                                 MATRIX_DESCR, SPARSE_MATRIX_TYPE_GENERAL, &
                                 mkl_sparse_d_create_coo, mkl_sparse_convert_csr, &
                                 mkl_sparse_destroy
        use mkl_sparse_qr, only: mkl_sparse_qr_reorder, &
                                 mkl_sparse_d_qr_factorize, mkl_sparse_d_qr_solve
        implicit none

        real(r_kind), intent(in)    :: Loss(n_x * net_size)
        real(r_kind), intent(inout) :: beta(n_neurons, net_size)
        real(r_kind)                :: dbeta(n_neurons, net_size)

        real(r_kind), dimension(:), allocatable :: alt_values
        integer :: stat
        type(SPARSE_MATRIX_T) :: A
        type(MATRIX_DESCR)    :: descr
        descr%type = SPARSE_MATRIX_TYPE_GENERAL


        stat = mkl_sparse_d_create_coo(A, SPARSE_INDEX_BASE_ONE, n_x * net_size, &
                                       n_neurons * net_size, nn, &
                                       sparse_rows, sparse_columns, jacobian_sparse)
        stat = mkl_sparse_convert_csr(A, SPARSE_OPERATION_NON_TRANSPOSE, A)
        stat = mkl_sparse_qr_reorder(A, descr)
        stat = mkl_sparse_d_qr_factorize(A, alt_values)
        stat = mkl_sparse_d_qr_solve(SPARSE_OPERATION_NON_TRANSPOSE, A, alt_values, &
                                     SPARSE_LAYOUT_COLUMN_MAJOR, 1, dbeta, &
                                     n_neurons * net_size, Loss, n_x * net_size)
        stat = mkl_sparse_destroy(A)
        deallocate(jacobian_sparse)
        deallocate(sparse_columns)
        deallocate(sparse_rows)
        beta = beta - dbeta

    end subroutine least_squares_sparse



    subroutine save_network_weight(bias, weight)
        implicit none

        real(r_kind), intent(in) :: bias(n_neurons)
        real(r_kind), intent(in) :: weight(n_neurons)

        character(len=8)   :: file_name = 'weig.txt'
        integer, parameter :: unit_number = 0
        integer            :: i


        call open_file(.true., file_name, unit_number)

        do i = 1, n_neurons
            write(unit_number, '(2(ES15.7,1X))') weight(i), bias(i)
        end do

        close(unit_number)

    end subroutine save_network_weight



    subroutine save_network_beta(step, beta, first)
        implicit none

        real(r_kind), intent(in) :: step
        real(r_kind), intent(in) :: beta(n_neurons, net_size)
        logical, intent(in)      :: first

        character(len=8) :: file_name = 'beta.txt'
        integer          :: unit_number = 0
        integer          :: i
        character(len=1) :: net_size_character
        real(r_kind)     :: betan(net_size)


        write(net_size_character, '(I1)') net_size

        call open_file(first, file_name, unit_number)

        write(unit_number, '((ES15.7,1X))') step

        do i = 1, n_neurons
            betan = beta(i, :)
            write(unit_number, '(' // net_size_character // '(ES15.7,1X))') betan
        end do

        close(unit_number)

    end subroutine save_network_beta



    subroutine open_file(first, file_name, unit_number)
        implicit none

        logical, intent(in)          :: first
        character(len=8), intent(in) :: file_name
        integer, intent(in)          :: unit_number
        integer                      :: f_status


        open(unit=unit_number, file=file_name, status='old', action='write', &
             iostat=f_status)
        if (f_status .ne. 0) then
            open(unit=unit_number, file=file_name, status='replace')
        else if (first) then
            close(unit_number)
            open(unit=unit_number, file=file_name, status='unknown', action='write', &
                 iostat=f_status)
        else
            close(unit_number)
            open(unit=unit_number, file=file_name, status='old', action='write', &
                 position='append')
        end if

    end subroutine open_file

end module xtfc_module

