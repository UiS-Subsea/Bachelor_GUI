global flag
flag = True


def toggle():
    global flag
    
    flag = not flag
    print(flag)