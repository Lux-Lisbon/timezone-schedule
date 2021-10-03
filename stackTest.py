class ArrayStack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.isEmpty():
          lastItem = self.stack[-1]
          del(self.stack[-1])
          return lastItem
    
    def isEmpty(self):
        return self.stack == []

    def stackPrinter(self):
        print(self.stack)

if __name__ == "__main__":
    s = ArrayStack()
    print("*"*5+"test"+5*"*")
    while(True):
        el = int(input("1 for Push\n2 for Pop\n3 to check if it is Empty\n4 to print Stack\n5 to exit\n"))
        if(el == 1):
            stackItem = input("Enter Item to push into the stack:\n")
            s.push(stackItem)
        if(el == 2):
            print(s.pop())
        if(el == 3):
            print(s.isEmpty())
        if(el == 4):
            s.stackPrinter()
        if(el == 5):
            break