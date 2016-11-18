dict = {'a':'123', 'b':'234'}
dict['c'] = '456'
dict['a'] = '456'
print dict

try:
    a = dict['d']
except KeyError:
    a = '0'

print a
