#   2       3      4      5      6       7      8        9       10
# 1.1 1.04779 1.0312 1.0231 1.0183 1.01514 1.0129 1.011231 1.009911
r = 1.009911

t = 0
step = 1e-12/60/60/24/365
tf = 1e4/60/60/24/365

file = open('trajectory_10', 'w')
file.write('''# time T rho    
# YRS/SEC; T8K/T9K; CGS/LOG 
# FORMAT: '(10x,A3)' 
# AGEUNIT = YRS 
# TUNIT   = T9K 
# RHOUNIT = CGS 
# ID = 0 \n''')
while t < tf:
    file.write('{:E}'.format(t) + '   3.000000E+00   1.000000E+09\n')
    t = t + step
    step = step*r
file.write('{:E}'.format(tf) + '   3.000000E+00   1.000000E+09\n')
file.close()



#                 1                 2                 3                 4
# 1.599858719606057 1.026913787832258 1.000380126854252 1.000004951757274
r = 1.000004951757274

t = 1e-5/60/60/24/365
tf = 4e3/60/60/24/365

file = open('trajectory_4', 'w')
file.write('''# time T rho    
# YRS/SEC; T8K/T9K; CGS/LOG 
# FORMAT: '(10x,A3)' 
# AGEUNIT = YRS 
# TUNIT   = T9K 
# RHOUNIT = CGS 
# ID = 0 \n''')
while t < tf:
    file.write('{:E}'.format(t) + '   1.0000000E+00  1.0000000E+00\n')
    t = t*r

file.write('{:E}'.format(tf) + '   1.0000000E+00  1.0000000E+00\n')
file.close()



r = 1.083

t = 0
step = 1e4/60/60/24/365
tf = 1e8/60/60/24/365

file = open('trajectory_1', 'w')
file.write('''# time T rho    
# YRS/SEC; T8K/T9K; CGS/LOG 
# FORMAT: '(10x,A3)' 
# AGEUNIT = YRS 
# TUNIT   = T9K 
# RHOUNIT = CGS 
# ID = 0 \n''')
while t < tf:
    file.write('{:E}'.format(t) + '   3.0000000E-07  1.0000000E+00\n')
    t = t + step
    step = step*r

file.write('{:E}'.format(tf) + '   3.0000000E-07  1.0000000E+00\n')
file.close()

