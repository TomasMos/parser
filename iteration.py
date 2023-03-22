def main():

    n = int(input("Height: "))
    draw(n)

def draw(n):

    
    if n == 0:
        return

    draw(n - 1)
    
    for i in range(n):
        print("#", end="")
    print("")


if __name__ == "__main__":
    main()
