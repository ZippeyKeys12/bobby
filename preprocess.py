import re

from strip import ZStript

IncludePattern = re.compile("\"(.+)\"\\s*", re.IGNORECASE)

ConfigPattern = re.compile(
    "\"(.+)\"\\s*(\\s|,)\\s*\"(.+)\"", re.IGNORECASE)


def ZPreprocess(FullFile, Data):
    Defines = {}
    Macros = {
        "include": ZPInclude,
        "define": ZPDefine,
        "undef": ZPUndef,
        "if": ZPIf,
        "ifdef": ZPIfDef,
        "ifndef": ZPIfNDef
    }
    Pattern = re.compile("#(\\w+)(\\s+(.*))?")
    Call = Pattern.search(FullFile)
    while Call:
        Result = Macros[Call.group(1).lower()](
            FullFile, Call.group(3), Defines, Data)
        if Result:
            FullFile = re.sub("#"+Call.group(1)+"\\s+" +
                              Result[0], Result[1]+"\n", FullFile)
        else:
            FullFile = re.sub(Call.group(0), "", FullFile)
        Call = Pattern.search(FullFile)
    # End
    return FullFile


def ZPInclude(FullFile, Args, Defines, Data):
    return (Args, ZStript(open(IncludePattern.match(Args.strip()).group(1)).read()))


def ZPConfig(FullFile, Args, Defines, Data):
    Call = ConfigPattern.match(Args.strip())
    return (Call.group(0), Data["CONFIG"][Call.group(1)][Call.group(3)])


def ZPDefine(FullFile, Args, Defines, Data):
    Defines[Args] = True


def ZPUndef(FullFile, Args, Defines, Data):
    Defines[Args] = False


def ZPIf(FullFile, Args, Defines, Data):
    return ""


def ZPIfDef(FullFile, Args, Defines, Data):
    return ""


def ZPIfNDef(FullFile, Args, Defines, Data):
    return ""
