import argparse

def f1():
    print("start running")

def save():
    print('save the data running')

def t1():
    parser= argparse.ArgumentParser()
    parser.add_argument('--start',action='store',help="Start the func",type=str)
    parser.add_argument('--save',help="Save the data or not",type=bool,default='false')
    args=parser.parse_args()
    print(type(args))
    start=args.start
    issave=args.save
    if start:
        f1()
        if issave:
             save()






if __name__ == '__main__':
    t1()