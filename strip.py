import re


def ZStript(FullFile, Whitespace=False, Comments=True):
    if Comments:
        # Block
        FullFile = re.sub(r"(?s)\/\*.*?\*\/", " ",
                          FullFile, flags=re.DOTALL | re.IGNORECASE)
        # Single-line
        FullFile = re.sub(r"\/\/+.*", " ", FullFile, flags=re.IGNORECASE)
    if Whitespace:
        FullFile = re.sub(r"\s+", " ", FullFile, flags=re.IGNORECASE)
        Tokens = ["{", "}", r"\(", r"\)", r"\[", r"\]", ";", ">", r"\*", "="]
        for Token in Tokens:
            FullFile = re.sub(
                r"\s*"+Token+r"\s*", Token.replace("\\", ""), FullFile, flags=re.IGNORECASE)
    return FullFile
