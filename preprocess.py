import re

from strip import ZStript

ConfigPattern = re.compile(r'"(.+)"\s*(\s|,)\s*"(.+)"')


def ZPreprocess(FullFile: str, Data: dict) -> str:
    FullFile = ZPConfigBlocks(FullFile)
    Defines = {}
    Macros = {
        "include": ZPInclude,
        "config": ZPConfig,
        "define": ZPDefine,
        "undef": ZPUndef,
        "if": ZPIf,
        "ifn": ZPIfN,
    }
    Pattern = re.compile(r"#(\w+)(\s+(.*))?")
    Call = Pattern.search(FullFile)
    while Call:
        if (Call.group(1) == "endif" or Call.group(1) == "region"
                or Call.group(1) == "endregion"):
            FullFile = re.sub(Call.group(0), "", FullFile)
        Result = Macros[Call.group(1)](FullFile, Call.group(3), Data, Defines)
        if Result:
            FullFile = FullFile.replace(Call.group(0), Result + "\n")
        else:
            FullFile = re.sub(Call.group(0), "", FullFile)
        Call = Pattern.search(FullFile)
    # End
    return FullFile


def ZPConfigBlocks(FullFile: str) -> str:
    # Config Blocks
    Pattern = re.compile(r"\[Config\](\s*){([^}]*)}", re.DOTALL)
    Call = Pattern.search(FullFile)
    while Call:
        Sections = Call.group(2).split(",")
        Replacement = ""
        for Section in Sections:
            Components = re.sub(r"\s+", " ", Section).split(":")
            Replacement += "const {}=\n#config {}\n;\n".format(
                Components[0].replace('"', ""), Components[1].replace(
                    ".", '","'))
        FullFile = re.sub(r"\[Config\](\s*){" + Call.group(2) + "}",
                          Replacement, FullFile)
        Call = Pattern.search(FullFile)
    return FullFile


IncludePattern = re.compile(r'"(.+)"\s*')


def ZPInclude(FullFile: str, Args: str, Data: dict, Defines: dict) -> str:
    return ZPConfigBlocks(
        ZStript(open(IncludePattern.match(Args.strip()).group(1)).read()))


def ZPConfig(FullFile: str, Args: str, Data: dict, Defines: dict) -> str:
    Call = ConfigPattern.match(Args.strip())
    return Data["CONFIG"][Call.group(1)][Call.group(3)]


def ZPDefine(FullFile: str, Args: str, Data: dict, Defines: dict) -> None:
    Defines[Args] = True


def ZPUndef(FullFile: str, Args: str, Data: dict, Defines: dict) -> None:
    if Args in Defines:
        del Defines[Args]


def ZPIf(FullFile: str, Args: str, Data: dict, Defines: dict):
    if Args not in Defines:
        FullFile = re.sub("#if\\s+" + Args, "", FullFile)


def ZPIfN(FullFile: str, Args: str, Data: dict, Defines: dict):
    pass
