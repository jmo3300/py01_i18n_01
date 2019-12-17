import os

def print_env_var(key):
    try:
        print(key + ": " + os.environ[key])
    except KeyError as ke:
        print("key {} not found".format(ke))


print_env_var('TEMP')
print_env_var('LANGUAGE')
print_env_var('LANG')
print_env_var('LC_MESSAGES')

