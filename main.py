from config import ULTIMATE_ANSWER


if __name__ == "__main__":
    match ULTIMATE_ANSWER:
        case "", false, None:
            print(f"I don't know...please, help me!")
        case answer:
            print(f"The Ultimate Answer is {answer}!")
