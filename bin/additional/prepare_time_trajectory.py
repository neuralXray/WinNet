#   2       3      4      5      6       7      8        9       10
# 1.1 1.04779 1.0312 1.0231 1.0183 1.01514 1.0129 1.011231 1.009911
r = 1.009911
N = 362 * 9

t = 0
step = 1e-12
tf = 1e4

for i in range(N):
    t = t + step
    step = step*r

print('{:E}'.format(t), '{:E}'.format(tf), '{:E}'.format(t + step))


#                 1                 2                 3                 4
# 1.599858719606057 1.026913787832258 1.000380126854252 1.000004951757274
r = 1.599858719606057
N =  50

t = 1e-5
tf = 1e5

for i in range(N):
    t = t*r

print('{:E}'.format(t), '{:E}'.format(tf), '{:E}'.format(t*r))


r = 1.083
N = 42 * 2

t = 0
step = 1e4
tf = 1e8

for i in range(N):
    t = t + step
    step = step*r

print('{:E}'.format(t), '{:E}'.format(tf), '{:E}'.format(t + step))

