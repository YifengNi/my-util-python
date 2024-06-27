def handle_command(command, params):
    if command == 'command1':
        print(f'Executing command1 with params: {params}')
        # 在这里添加command1的实现
    elif command == 'command2':
        print(f'Executing command2 with params: {params}')
        # 在这里添加command2的实现
    else:
        print(f'Unknown command: {command}')

while True:
    user_input = input('Enter command: ')
    if user_input == 'exit':
        break

    split_input = user_input.split(' ')
    command = split_input[0]
    params = split_input[1:]

    handle_command(command, params)