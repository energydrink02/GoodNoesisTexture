from inc_noesis import *
#from typing import Optional, Dict

def registerNoesisTypes():
    handle = noesis.register("GoodEngine Archive", ".ho")
    noesis.setHandlerExtractArc(handle, extractAllTextures)
    
    handle = noesis.register("GoodEngine Xbox360 Texture", ".ptex_xenon")
    noesis.setHandlerTypeCheck(handle, noepyCheckXenonType)
    noesis.setHandlerLoadRGBA(handle, goodLoadXenon)

    handle = noesis.register("GoodEngine PS3 Texture", ".ptex_ps3")
    noesis.setHandlerTypeCheck(handle, noepyCheckPS3Type)
    noesis.setHandlerLoadRGBA(handle, goodLoadPS3)

    handle = noesis.register("GoodEngine Wii Texture", ".ptex_wii")
    noesis.setHandlerTypeCheck(handle, noepyCheckWiiType)
    noesis.setHandlerLoadRGBA(handle, goodLoadWii)
    
    return 1

# ------------------------------------------------------------
#                         - Xbox 360 -
# ------------------------------------------------------------                            

GPUTEXTUREFORMAT_1_REVERSE = 0
GPUTEXTUREFORMAT_1 = 1
GPUTEXTUREFORMAT_8 = 2
GPUTEXTUREFORMAT_1_5_5_5 = 3
GPUTEXTUREFORMAT_5_6_5 = 4
GPUTEXTUREFORMAT_6_5_5 = 5
GPUTEXTUREFORMAT_8_8_8_8 = 6
GPUTEXTUREFORMAT_2_10_10_10 = 7
GPUTEXTUREFORMAT_8_A = 8
GPUTEXTUREFORMAT_8_B = 9
GPUTEXTUREFORMAT_8_8 = 10
GPUTEXTUREFORMAT_Cr_Y1_Cb_Y0_REP = 11
GPUTEXTUREFORMAT_Y1_Cr_Y0_Cb_REP = 12
GPUTEXTUREFORMAT_16_16_EDRAM = 13
GPUTEXTUREFORMAT_8_8_8_8_A = 14
GPUTEXTUREFORMAT_4_4_4_4 = 15
GPUTEXTUREFORMAT_10_11_11 = 16
GPUTEXTUREFORMAT_11_11_10 = 17
GPUTEXTUREFORMAT_DXT1 = 18
GPUTEXTUREFORMAT_DXT2_3 = 19
GPUTEXTUREFORMAT_DXT4_5 = 20
GPUTEXTUREFORMAT_16_16_16_16_EDRAM = 21
GPUTEXTUREFORMAT_24_8 = 22
GPUTEXTUREFORMAT_24_8_FLOAT = 23
GPUTEXTUREFORMAT_16 = 24
GPUTEXTUREFORMAT_16_16 = 25
GPUTEXTUREFORMAT_16_16_16_16 = 26
GPUTEXTUREFORMAT_16_EXPAND = 27
GPUTEXTUREFORMAT_16_16_EXPAND = 28
GPUTEXTUREFORMAT_16_16_16_16_EXPAND = 29
GPUTEXTUREFORMAT_16_FLOAT = 30
GPUTEXTUREFORMAT_16_16_FLOAT = 31
GPUTEXTUREFORMAT_16_16_16_16_FLOAT = 32
GPUTEXTUREFORMAT_32 = 33
GPUTEXTUREFORMAT_32_32 = 34
GPUTEXTUREFORMAT_32_32_32_32 = 35
GPUTEXTUREFORMAT_32_FLOAT = 36
GPUTEXTUREFORMAT_32_32_FLOAT = 37
GPUTEXTUREFORMAT_32_32_32_32_FLOAT = 38
GPUTEXTUREFORMAT_32_AS_8 = 39
GPUTEXTUREFORMAT_32_AS_8_8 = 40
GPUTEXTUREFORMAT_16_MPEG = 41
GPUTEXTUREFORMAT_16_16_MPEG = 42
GPUTEXTUREFORMAT_8_INTERLACED = 43
GPUTEXTUREFORMAT_32_AS_8_INTERLACED = 44
GPUTEXTUREFORMAT_32_AS_8_8_INTERLACED = 45
GPUTEXTUREFORMAT_16_INTERLACED = 46
GPUTEXTUREFORMAT_16_MPEG_INTERLACED = 47
GPUTEXTUREFORMAT_16_16_MPEG_INTERLACED = 48
GPUTEXTUREFORMAT_DXN = 49
GPUTEXTUREFORMAT_8_8_8_8_AS_16_16_16_16 = 50
GPUTEXTUREFORMAT_DXT1_AS_16_16_16_16 = 51
GPUTEXTUREFORMAT_DXT2_3_AS_16_16_16_16 = 52
GPUTEXTUREFORMAT_DXT4_5_AS_16_16_16_16 = 53
GPUTEXTUREFORMAT_2_10_10_10_AS_16_16_16_16 = 54
GPUTEXTUREFORMAT_10_11_11_AS_16_16_16_16 = 55
GPUTEXTUREFORMAT_11_11_10_AS_16_16_16_16 = 56
GPUTEXTUREFORMAT_32_32_32_FLOAT = 57
GPUTEXTUREFORMAT_DXT3A = 58
GPUTEXTUREFORMAT_DXT5A = 59
GPUTEXTUREFORMAT_CTX1 = 60
GPUTEXTUREFORMAT_DXT3A_AS_1_1_1_1 = 61
GPUTEXTUREFORMAT_8_8_8_8_GAMMA_EDRAM = 62
GPUTEXTUREFORMAT_2_10_10_10_FLOAT_EDRAM = 63

GPUENDIAN_NONE = 0
GPUENDIAN_8IN16 = 1
GPUENDIAN_8IN32 = 2
GPUENDIAN_16IN32 = 3

class GPUTEXTURESIZE:
    def __init__(self, val: int):
        self._val = val

    def get2D(self):
        return ((self._val & 0x1FFF) + 1, ((self._val >> 13) & 0x1FFF) + 1)
    
class D3DBaseTexture:
    def __init__(self, bs: NoeBitStream):
        self.Resource = D3DResource(bs)
        self.MipFlush = bs.readUInt()
        self.Format = GPUTEXTURE_FETCH_CONSTANT(bs)
    
class D3DResource:
    def __init__(self, bs: NoeBitStream):
        self.Common = bs.readUInt()
        self.ReferenceCount = bs.readUInt()
        self.Fence = bs.readUInt()
        self.ReadFence = bs.readUInt()
        self.Identifier = bs.readUInt()
        self.BaseFlush = bs.readUInt()

class GPUTEXTURE_FETCH_CONSTANT:
    def __init__(self, bs: NoeBitStream):
        dword0 = bs.readUInt()
        self.Tiled = ((dword0 >> 31) & 1) != 0
        self.Pitch = (dword0 >> 22) & 0x3FF
        self.MultiSample = (dword0 >> 19) & 3
        self.ClampZ = (dword0 >> 16) & 7
        self.ClampY = (dword0 >> 13) & 7
        self.ClampX = (dword0 >> 10) & 7
        self.SignW = (dword0 >> 8) & 3
        self.SignZ = (dword0 >> 6) & 3
        self.SignY = (dword0 >> 4) & 3
        self.SignX = (dword0 >> 2) & 3
        self.ConstantType = dword0 & 3

        dword1 = bs.readUInt()
        self.BaseAddress = dword1 >> 12
        self.ClampPolicy = (dword1 >> 11) & 1
        self.Stacked = ((dword1 >> 10) & 1) != 0
        self.RequestSize = (dword1 >> 8) & 3
        self.Endian = (dword1 >> 6) & 3
        self.DataFormat = dword1 & 0x3F

        dword2 = bs.readUInt()
        self.Size = GPUTEXTURESIZE(dword2)

        dword3 = bs.readUInt()
        self.BorderSize = ((dword3 >> 28) & 1) != 0
        self.AnisoFilter = (dword3 >> 25) & 7
        self.MipFilter = (dword3 >> 23) & 3
        self.MinFilter = (dword3 >> 21) & 3
        self.MagFilter = (dword3 >> 19) & 3
        self.ExpAdjust = (dword3 >> 13) & 0x3F
        self.SwizzleW = (dword3 >> 10) & 7
        self.SwizzleZ = (dword3 >> 7) & 7
        self.SwizzleY = (dword3 >> 4) & 7
        self.SwizzleX = (dword3 >> 1) & 7
        self.NumFormat = dword3 & 1

        dword4 = bs.readUInt()
        self.GradExpAdjustH = (dword4 >> 27) & 0x1F
        self.GradExpAdjustV = (dword4 >> 22) & 0x1F
        self.LODBias = (dword4 >> 12) & 0x3FF
        self.MinAnisoWalk = ((dword4 >> 11) & 1) != 0
        self.MagAnisoWalk = ((dword4 >> 10) & 1) != 0
        self.MaxMipLevel = (dword4 >> 6) & 0xF
        self.MinMipLevel = (dword4 >> 2) & 0xF
        self.VolMinFilter = (dword4 >> 1) & 1
        self.VolMagFilter = dword4 & 1

        dword5 = bs.readUInt()
        self.MipAddress = dword5 >> 12
        self.PackedMips = ((dword5 >> 1) & 1) != 0
        self.Dimension = (dword5 >> 9) & 3
        self.AnisoBias = (dword5 >> 5) & 0xF
        self.TriClamp = (dword5 >> 3) & 3
        self.ForceBCWToMax  = ((dword5 >> 1) & 1) != 0
        self.BorderColor = dword5 & 3

def noepyCheckXenonType(data):
    return 1
    
def goodLoadXenon(data, texList):
    bs = NoeBitStream(data, NOE_BIGENDIAN)
    baseTexture = D3DBaseTexture(bs) 
    bs.seek(0x38) 

    texelPitch = {
        GPUTEXTUREFORMAT_DXT1: 8,
        GPUTEXTUREFORMAT_DXT2_3 : 16,
        GPUTEXTUREFORMAT_DXT4_5 : 16
    }

    d3dToNoesis = {
        GPUTEXTUREFORMAT_DXT1: noesis.NOESISTEX_DXT1,
        GPUTEXTUREFORMAT_DXT2_3: noesis.NOESISTEX_DXT3,
        GPUTEXTUREFORMAT_DXT4_5: noesis.NOESISTEX_DXT5,
        GPUTEXTUREFORMAT_8_8_8_8: noesis.NOESISTEX_RGBA32,
    }
    
    pixelBuf = bs.readBytes(bs.getSize() - bs.tell())
    width, height = baseTexture.Format.Size.get2D()

    if baseTexture.Format.Endian == GPUENDIAN_8IN16:
        pixelBuf = rapi.swapEndianArray(pixelBuf, 2)

    if baseTexture.Format.DataFormat == GPUTEXTUREFORMAT_8_8_8_8:
        texData = rapi.imageUntile360Raw(pixelBuf, width, height, 4)
    else:
        texData = rapi.imageUntile360DXT(pixelBuf, width, height, texelPitch[baseTexture.Format.DataFormat])

    texList.append(NoeTexture(rapi.getInputName(), width, height, texData, d3dToNoesis[baseTexture.Format.DataFormat]))
    
    return 1


# ------------------------------------------------------------
#                           - PS3 -                            
# ------------------------------------------------------------   

class DDS_PIXELFORMAT:
    def __init__(self, bs: NoeBitStream):
        self.dwSize = bs.readUInt()
        self.dwFlags = bs.readUInt()
        self.dwFourCC = bs.readUInt()
        self.dwRGBBitCount = bs.readUInt()
        self.dwRBitMask = bs.readUInt()
        self.dwGBitMask = bs.readUInt()
        self.dwBBitMask = bs.readUInt()
        self.dwABitMask = bs.readUInt()

    def write(self, bs: NoeBitStream):
        bs.writeUInt(self.dwSize)
        bs.writeUInt(self.dwFlags)
        bs.writeUInt(self.dwFourCC)
        bs.writeUInt(self.dwRGBBitCount)
        bs.writeUInt(self.dwRBitMask)
        bs.writeUInt(self.dwGBitMask)
        bs.writeUInt(self.dwBBitMask)
        bs.writeUInt(self.dwABitMask)


class DDS_HEADER:
    def __init__(self, bs: NoeBitStream):
        self.magic = bs.readUInt()
        self.dwSize = bs.readUInt()
        self.dwFlags = bs.readUInt()
        self.dwHeight = bs.readUInt()
        self.dwWidth = bs.readUInt()
        self.dwPitchOrLinearSize = bs.readUInt()
        self.dwDepth = bs.readUInt()
        self.dwMipMapCount = bs.readUInt()
        self.dwReserved1 = bs.readBytes(4 * 11)
        self.ddspf = DDS_PIXELFORMAT(bs)
        self.dwCaps = bs.readUInt()
        self.dwCaps2 = bs.readUInt()
        self.dwCaps3 = bs.readUInt()
        self.dwCaps4 = bs.readUInt()
        self.dwReserved2 = bs.readUInt()

    def write(self) -> bytes:
        bs = NoeBitStream()
        bs.writeUInt(self.magic)
        bs.writeUInt(self.dwSize)
        bs.writeUInt(self.dwFlags)
        bs.writeUInt(self.dwHeight)
        bs.writeUInt(self.dwWidth)
        bs.writeUInt(self.dwPitchOrLinearSize)
        bs.writeUInt(self.dwDepth)
        bs.writeUInt(self.dwMipMapCount)
        bs.writeBytes(self.dwReserved1)
        self.ddspf.write(bs)
        bs.writeUInt(self.dwCaps)
        bs.writeUInt(self.dwCaps2)
        bs.writeUInt(self.dwCaps3)
        bs.writeUInt(self.dwCaps4)
        bs.writeUInt(self.dwReserved2)

        return bs.getBuffer()
    
def noepyCheckPS3Type(data):
    bs = NoeBitStream(data, NOE_BIGENDIAN)
    return bs.readUInt() == 0x20534444

def goodLoadPS3(data, texList):
    bs = NoeBitStream(data, NOE_BIGENDIAN)

    dds_header = DDS_HEADER(bs)   
    pixelbuf = bs.readBytes(bs.getSize() - bs.tell())

    # Convert big-endian dds header to little-endian
    data = dds_header.write() + pixelbuf
    
    texture = rapi.loadTexByHandler(data, ".dds")
    texList.append(texture)
    return 1
    
# ------------------------------------------------------------
#                           - WII -                            
# ------------------------------------------------------------   

class WiiTextureFileHeader:
    def __init__(self, bs: NoeBitStream):
        self.TextureType = bs.readUInt()
        self.AlphaScale = bs.readUInt()
        self.NumTextures = bs.readUShort()
        self.MaxAniso = bs.read(">6B")
        bs.seek(0x10, NOESEEK_REL)

def noepyCheckWiiType(data):
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "lib_zq_nintendo_tex.py")):
        return False
    
    bs = NoeBitStream(data, NOE_BIGENDIAN)
    bs.seek(0x20)
    return bs.readUInt() == 0x0020AF30

def goodLoadWii(data, texList):
    import lib_zq_nintendo_tex as nintex
    bs = NoeBitStream(data, NOE_BIGENDIAN)

    # Heavy Iron Header
    wiiTextureHeader = WiiTextureFileHeader(bs)

    # Nintendo TPL Header
    magic = bs.readUInt()
    count = bs.readUInt()
    imageTblAddr = bs.readUInt()

    bs.seek(imageTblAddr + 0x20)
    data = [{
        'imageDataAddr':  bs.readUInt(),
        'imagePaletteAddr': bs.readUInt()
    } for i in range(count)]

    for x in data:
        paletteBuffer = None
        paletteFormat = None

        if x['imagePaletteAddr']:
            bs.seek(x['imagePaletteAddr'] + 0x20)
            palette = {
                'num':      bs.readUShort(),
                'unpacked': bs.readUByte(),
                'junk':     bs.readUByte(),
                'format':   bs.readUInt(),
                'addr':     bs.readUInt()
            }
            paletteBuffer = bs.getBuffer(palette['addr'], palette['addr'] + nintex.getPaletteSizeInBytes(palette['format'], palette['num']))
            paletteFormat = palette['format']

        bs.seek(x['imageDataAddr'] + 0x20)
        image = {
            'height':        bs.readUShort(),
            'width':         bs.readUShort(),
            'format':        bs.readUInt(),
            'addr':          bs.readUInt(),
            'wrapS':         bs.readUInt(),
            'wrapT':         bs.readUInt(),
            'minFilter':     bs.readUInt(),
            'magFilter':     bs.readUInt(),
            'lodBias':       bs.readFloat(),
            'edgeLodEnable': bs.readUByte(),
            'minLod':        bs.readUByte(),
            'maxLod':        bs.readUByte(),
            'unpacked':      bs.readUByte(),
        }

        bs.seek(image['addr'] + 0x20)
        tex = nintex.readTexture(bs, image['width'], image['height'], image['format'], paletteBuffer, paletteFormat)
        texList.append(tex)

    return len(texList)


# ------------------------------------------------------------
#                       - HO Archive -                            
# ------------------------------------------------------------

def ReadWideString(bs: NoeFileStream, char_amount):
    string = ""
    for c in range(char_amount):
        integ = bs.readUShort()
        if integ != 0: string += chr(integ)
    return string

def ReadUntil(bs: NoeFileStream, terminator = b"\x00"):
    string = ""
    while True:
        char = bs.readBytes(1)
        if char == terminator:
            break
        string += char.decode("utf-8")
    return string

SECTIONTYPE_P = 0x50202020
SECTIONTYPE_PD = 0x50442020
SECTIONTYPE_PTEX = 0x50544558
SECTIONTYPE_PFST = 0x50465354

SLICETYPE_TOC = 0
SLICETYPE_DATA = 1
SLICETYPE_PADDING = 2

class MetaParcelSlicesEntry:
    def __init__(self, bs: NoeFileStream):
        self.sliceType = bs.readUInt()
        self.sliceStart = bs.readUInt()
        self.sliceSize = bs.readUInt()
        self.sliceAlign = bs.readUInt()

class ParcelSliceMeta:
    def __init__(self, bs: NoeFileStream):
        self.metatype = bs.readBytes(4).decode("utf-8")
        self.metasize = bs.readUInt()
        self.numSlices = bs.readUInt()
        bs.readUInt()

        self.slices = [MetaParcelSlicesEntry(bs) for _ in range(self.numSlices)]

class ParcelSliceDebugMeta:
    def __init__(self, bs: NoeFileStream):
        self.magic = bs.readBytes(4).decode("utf-8")
        self.size = bs.readUInt()
        self.count = bs.readUInt()
        self.offset = bs.readUInt()
        bs.readBytes(0x10)

class PSLDEntry:
    def __init__(self, bs: NoeFileStream):
        self.uid = bs.readUInt64()
        self.offset = bs.readUInt()
        bs.readBytes(0x14)
        self.assetname = ReadUntil(bs)

class TOCEntry:
    def __init__(self, bs: NoeFileStream):
        self.elementSize = bs.readUInt()
        self.elementOffset = bs.readUInt()
        self.blobSize = bs.readUInt()
        self.blobAlign = bs.readUInt()
        self.uidSelf = bs.readUInt64()
        self.wmlTypeID = bs.readUInt()
        self.subType = bs.readUShort()
        self.blobFlags = bs.readUShort()

        self.data = b""

class TableHeader:
    def __init__(self, bs: NoeFileStream):
        self.tableTypeTag = bs.readBytes(4).decode("utf-8")
        self.entryCount = bs.readUInt()
        self.tableFlags = bs.readUInt()
        self.firstString = bs.readUInt()
        self.stringTableSize = bs.readUInt()
        self.firstMetaRec = bs.readUInt()
        self.metaDataSize = bs.readUInt()
        bs.readUInt()

class SectionEntry:
    def __init__(self, bs: NoeFileStream):
        self.meta = None #: Optional[ParcelSliceDebugMeta, ParcelSliceMeta] = None

        self.sectionType = bs.readUInt()
        self.packLangID = bs.readUShort()
        self.parcelType = bs.readUByte()
        bs.readByte()
        self.userKey = bs.readUInt()
        self.nameHash = bs.readUInt()
        self.namePtr = bs.readUInt()
        self.fromNameHash = bs.readUInt()
        self.fromNamePtr = bs.readUInt()
        self.startSector = bs.readUInt()
        self.sizeOnDisk = bs.readUInt()
        self.sizeInMem = bs.readUInt()
        self.memoryAlignment = bs.readUInt()
        self.attributeFlags = bs.readUInt()
        self.externName = bs.readUInt()
        self.metaBlockCount = bs.readUInt()
        self.metaRecord = bs.readUInt()
        bs.readUInt()

class HO:
    def __init__(self, bs: NoeFileStream):
        self.bs = bs

        self.assetNames = {}
        self.assets = {} #: Dict[int, TOCEntry] = {}

        bs.seek(0x40)
        self.sectorSize = bs.readUInt()
        self.startSector = bs.readUInt()
        self.tableSize = bs.readUInt()

        bs.seek(0x400)
        self.platform = ReadWideString(bs, 0x1E)

        bs.seek(0x47C)
        self.target = ReadWideString(bs, 0x20)

        self.goToSector(self.startSector)
        self.masterTableHeader = TableHeader(bs)
        self.masterTableEntry = SectionEntry(bs)

        startSectionTable = self.goToSector(self.masterTableEntry.startSector)
        self.SectionTableHeader = TableHeader(bs)
        self.Parcels = [SectionEntry(bs) for _ in range(self.SectionTableHeader.entryCount)]

        for parcel in self.Parcels:
            self.bs.seek(startSectionTable + parcel.metaRecord)

            if parcel.sectionType == SECTIONTYPE_PD:
                parcel.meta = ParcelSliceDebugMeta(bs)
            else:
                parcel.meta = ParcelSliceMeta(bs)

        for parcel in self.Parcels:
            startParcel = self.goToSector(parcel.startSector)

            if isinstance(parcel.meta, ParcelSliceDebugMeta):
                entrySizes = [bs.readUInt() for _ in range(parcel.meta.count)]
                self.bs.seek(startParcel + parcel.meta.offset)

                for x in range(len(entrySizes)):
                    start = self.bs.tell()
                    psldEntry = PSLDEntry(bs)
                    self.assetNames[psldEntry.uid] = psldEntry.assetname
                    self.bs.seek(start + entrySizes[x])
            elif isinstance(parcel.meta, ParcelSliceMeta):
                for slice in parcel.meta.slices:
                    if slice.sliceType != SLICETYPE_TOC:
                        continue
                    self.bs.seek(startParcel + slice.sliceStart)

                    elementCount = bs.readUInt()
                    brickDataOffset = bs.readUInt()
                    self.bs.seek(0x18, NOESEEK_REL)

                    tocEntries = [TOCEntry(bs) for _ in range(elementCount)]
                    for asset in tocEntries:
                        self.bs.seek(startParcel + asset.elementOffset)
                        asset.data = bs.readBytes(asset.blobSize)

                        self.assets[asset.uidSelf] = asset

    def goToSector(self, sector) -> int:
        self.bs.seek(sector * self.sectorSize)
        return self.bs.tell()
                
TEXTURE = 0x2952081F
GEN_TEXTURERESOURCE = 0xE9AA3502

def extractAllTextures(fileName, fileLen, justChecking):
    if justChecking:
        return 1
    
    file = open(fileName, "rb")
    hoe = HO(NoeFileStream(file, NOE_BIGENDIAN))

    game = hoe.target.lower()
    platform = hoe.platform.lower()
    assettype = [TEXTURE, GEN_TEXTURERESOURCE]

    for asset in hoe.assets.values():
        if asset.wmlTypeID not in assettype:
            continue

        assetname = hoe.assetNames.get(asset.uidSelf, hex(asset.uidSelf))

        rawblob_asset = hoe.assets.get(int.from_bytes(asset.data[:8], "big"), None)
        if rawblob_asset == None:
            continue

        if platform == "xenon":
            # Xbox header in Texture
            data = asset.data[0x8 if game == "rats" else 0x10:] + rawblob_asset.data
        else:
            # DDS (PS3) and Wii header in RawBlob
            data = rawblob_asset.data

        output_ext = ".ptex_" + platform
        
        noesis.logOutput("Exporting Texture: " +  assetname + "[" + hex(asset.uidSelf) + "]" + "\n")
        rapi.exportArchiveFile(assetname + "_" + hex(asset.uidSelf)[2:].rjust(16, '0') + output_ext, data)

    return 1