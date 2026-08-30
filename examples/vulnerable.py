def unsafe_buffer_op(user_input):
    buffer = [0] * 10
    index = int(user_input)
    buffer[index] = 42
    return buffer

def race_condition_demo():
    shared_var = 0
    def increment():
        global shared_var
        temp = shared_var
        temp += 1
        shared_var = temp
    return increment

def sql_injection_example(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query
