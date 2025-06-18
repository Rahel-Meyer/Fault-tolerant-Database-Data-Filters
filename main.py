import Tests


def main():
    print("Welcome to the experiment! Please choose an option:")
    print("1: Calculate confusion matrix")
    print("2: Calculate statistical values")

    option = input("Enter your choice (1 or 2): ")

    opti = input("Would you like to use the majority-based optimization? (y/n): ").strip().lower()
    if opti not in ['y', 'n']:
        print("Invalid input! Please answer with 'y' or 'n'.")
        return

    n = int(input("Enter the value for n (length of input): "))
    k = int(input("Enter the value for k (number of characters per prefix): "))
    num_iterations = int(input("Enter the number of iterations: "))

    if opti == 'y':
        d = int(input("Enter the value for d (number of duplicates per character): "))
        b = 8
    else:
        d = 1
        inputdata = input("Would you like to use a realistic character distribution as input? (y/n): ")
        if inputdata not in ['y', 'n']:
            print("Invalid input! Please answer with 'y' or 'n'.")
            return
        if inputdata == 'y':
            b = 5
        else:
            b = 8

    if option == '1':
        Tests.see_confusion_matrix(num_iterations, n, k, b, d, opti == 'y')

    elif option == '2':
        Tests.see_stats(n, k, b, d, num_iterations, opti == 'y')

    else:
        print("Invalid input! Please choose either 1 or 2.")


if __name__ == '__main__':
    main()
