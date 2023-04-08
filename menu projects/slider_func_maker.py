v_name = input('What is the var name >>> ')
start_val = input('What is the starting value of the var >>> ')
min_val = input('What is the min value of the var >>> ')
max_val = input('What is the max value of the var >>> ')
print(f'{v_name} = {start_val}')
print(f'def {v_name}_slider_func(set_get):')
print(f'    global {v_name}')
print(f'    ')
print(f'    var_min = {min_val}')
print(f'    var_max = {max_val}')
print(f"    if set_get == 'get':")
print(f"        return ({v_name}-var_min)/(var_max-var_min)")
print(f'    else:')
print(f'        {v_name} = var_min+((var_max-var_min)*set_get)')





ex_slider_var = 0
def ex_slider_func(set_get):

    global ex_slider_var
    var_min = -1
    var_max = 2

    if set_get == 'get':
        return (ex_slider_var-var_min)/(var_max-var_min)
    else:
        ex_slider_var = var_min+((var_max-var_min)*set_get)