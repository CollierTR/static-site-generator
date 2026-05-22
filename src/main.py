from textnode import TextNode, TextType
 
def main():
    """Entry point of the application. Creates a TextNode and prints it."""
    node = TextNode("This is dummy text!", TextType.PLAIN_TEXT)
    print(node)

main()
