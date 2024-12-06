from textnode import TextNode, TextType


def main():
    tn1 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    tn2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
    tn3 = TextNode("Node without url", TextType.NORMAL)

    print(tn1)
    print(tn2)
    print(tn1 == tn2)
    print(tn3)


if __name__ == "__main__":
    main()
