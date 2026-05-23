from data.models import AGGFrame, ACCFrame, GNSSFrame

def nmea_to_decimal(value: str, direction: str) -> float:
    dot = value.index(".")
    degrees = float(value[:dot - 2])
    minutes = float(value[dot - 2:])
    decimal = degrees + minutes / 60.0
    if direction in ("S", "W"):
        decimal = -decimal
    return decimal

def parse_line(line: str) -> AGGFrame | ACCFrame | GNSSFrame | None:
    parts = line.strip().split(",")

    if len(parts)<=2:
        return None

    header = parts[0]
    try:
        if header == "$AGG" and len(parts) >=5:
            return AGGFrame(float(parts[1]),float(parts[2]),float(parts[3]),int(parts[4]))
        if header == "$ACC" and len(parts) >=5:
            return ACCFrame(float(parts[1]),float(parts[2]),float(parts[3]),int(parts[4]))
        if header == "$GNGGA" and len(parts) >= 10:
            if parts[6] == "0" or parts[2] == "":
                return None
            return GNSSFrame(
            timestamp   = parts[1],
            lat         = nmea_to_decimal(parts[2], parts[3]),
            lon         = nmea_to_decimal(parts[4], parts[5]),
            fix_quality = int(parts[6]),
            num_sats    = int(parts[7]),
            hdop        = float(parts[8]),
            altitude    = float(parts[9])
        )
    except ValueError:
        return None
    
    return None
        


    
