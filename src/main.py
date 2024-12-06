from textnode import TextNode, TextType


def main():
    tn1 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    tn2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")

    print(tn1)
    print(tn2)
    print(tn1 == tn2)


if __name__ == "__main__":
    main()
