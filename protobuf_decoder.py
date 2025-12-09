# filename: protobuf_decoder/protobuf_decoder.py

import struct
from google.protobuf.internal import decoder

class ParsedResult:
    def __init__(self, field, wire_type, data):
        self.field = field
        self.wire_type = wire_type
        self.data = data

class ParseResultData:
    def __init__(self, results):
        self.results = results

class Parser:
    def parse(self, data):
        if isinstance(data, str):
            try:
                data = bytes.fromhex(data)
            except:
                pass
        
        results = []
        pos = 0
        length = len(data)
        
        while pos < length:
            try:
                (tag, pos) = decoder._DecodeVarint(data, pos)
            except IndexError:
                break
                
            field_number = tag >> 3
            wire_type = tag & 7
            
            if wire_type == 0: # Varint
                (value, pos) = decoder._DecodeVarint(data, pos)
                results.append(ParsedResult(str(field_number), "varint", value))
                
            elif wire_type == 2: # Length Delimited
                (size, pos) = decoder._DecodeVarint(data, pos)
                if pos + size > length:
                    break
                value = data[pos : pos + size]
                pos += size
                
                # Try to recursively parse (Nested message)
                try:
                    sub_parser = Parser()
                    sub_results = sub_parser.parse(value)
                    if sub_results:
                        results.append(ParsedResult(str(field_number), "length_delimited", ParseResultData(sub_results)))
                    else:
                         # Fallback to string/bytes if not parseable as message
                        try:
                            str_val = value.decode('utf-8')
                            results.append(ParsedResult(str(field_number), "string", str_val))
                        except:
                            results.append(ParsedResult(str(field_number), "bytes", value.hex()))
                except:
                     results.append(ParsedResult(str(field_number), "bytes", value.hex()))

            elif wire_type == 1: # 64-bit
                if pos + 8 > length:
                    break
                value = data[pos : pos + 8]
                pos += 8
                results.append(ParsedResult(str(field_number), "fixed64", value.hex()))
                
            elif wire_type == 5: # 32-bit
                if pos + 4 > length:
                    break
                value = data[pos : pos + 4]
                pos += 4
                results.append(ParsedResult(str(field_number), "fixed32", value.hex()))
                
            else:
                # Unknown wire type, stop parsing
                break
                
        return results
        