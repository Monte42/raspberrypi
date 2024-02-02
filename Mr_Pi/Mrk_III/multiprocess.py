import multiprocessing as mp 
import time



def scan():
    i = 0
    while scanning:
        i += 1
        time.sleep(1)
    print(i)

def my_controller():
    print('hello')
    x = input()
    if x == 'y':
        return False

    

if __name__ == '__main__':
    scanning = True
    p2 = mp.Process(target=scan, args=())
    p2.start()
    scanning = my_controller()
    