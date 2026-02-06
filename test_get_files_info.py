from functions.get_files_info import get_files_info

def main():
    # 1. current dir
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(f"  {result.replace('\n', '\n  ')}")

    # 2. 'pkg' dir
    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(f"  {result.replace('\n', '\n  ')}")

    # 3. '/bin' dir
    result = get_files_info("calculator", "/bin")
    print("Result for '/bin' directory:")
    print(f"  {result.replace('\n', '\n  ')}")

    # 4. '../' dir
    result = get_files_info("calculator", "../")
    print("Result for '../' directory:")
    print(f"  {result.replace('\n', '\n  ')}")

if __name__ == "__main__":
    main()