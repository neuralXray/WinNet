#!/bin/bash
# Author: M. Reichert
# Date: 10.1.23
# Updated: 14.11.23: Carlos Rábano

echo "Script to setup WinNet on Linux with apt package manager."
echo "This script is installing all necessary python packages in a new venv called 'winnet',"
echo "the Intel Fortran Compiler and the Intel oneAPI Math Kernel Library."
echo "Use on your own risk!"
while true; do
read -p "Do you want to proceed? (y/n) " yn
case $yn in
	[yY] ) echo ok, we will proceed;
		break;;
	[nN] ) echo exiting...;
		exit;;
	* ) echo invalid response;;
esac
done


# Create and activate an empty venv
echo ""
echo "##############################"
echo "python3 -m venv ../winnet"
echo "##############################"
echo ""
python3 -m venv ../winnet
echo ""
echo "##############################"
echo "source ../winnet/bin/activate"
echo "##############################"
echo ""
source ../winnet/bin/activate
# Now install all needed packages
echo ""
echo "##############################"
echo "python -m pip install -r requirements_tested.txt"
echo "##############################"
echo ""
python -m pip install -r requirements.txt


# If ifort does not exist install it
if ! command -v ifx &> /dev/null
then
    wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
    echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list
	sudo apt update
	sudo apt install intel-oneapi-common-vars intel-oneapi-compiler-fortran intel-oneapi-mkl intel-oneapi-mkl-devel

    echo 'source /opt/intel/oneapi/setvars.sh' >> ~/.bashrc
    source ~/.bashrc

fi


# echo 'export OMP_NUM_THREADS=1' >> ~/.bashrc


# Say a bit more on the usage
echo "---"
echo ""
echo ""
echo "Fully installed. Use the python environment 'winnet'."
echo "Activate with:"
echo ""
echo "source winnet/bin/activate"
echo ""
echo "before using the makerun.py"

