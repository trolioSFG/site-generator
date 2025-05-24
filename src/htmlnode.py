class HTMLNode():
    tag = ''
    value = ''
    children = []
    props = {}

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        html = ''
        if self.props:
            for k,v in self.props.items():
                html += f' {k}="{v}"'
        return html

    def __repr__(self):
        rep = 'HTMLNode('
        rep += f"{self.tag}, {self.value}, children: "
        if self.children:
            for child in self.children:
                rep += f"({child.tag}, {child.value}) "
        else:
            rep += str(self.children)

        rep += ", " + str(self.props) + ")"

        return rep

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode without value")

        if self.tag is None:
            return str(self.value)

        # Special CASE ?
        if self.tag == "img":
            return "<" + self.tag + self.props_to_html() + ">"


        return "<" + self.tag + self.props_to_html() + f">{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode with no tag")

        if self.children is None:
            raise ValueError("ParentNode without children")

        rep = f"<{self.tag}>"
        for child in self.children:
            rep += child.to_html()
        rep += f"</{self.tag}>"
        return rep



