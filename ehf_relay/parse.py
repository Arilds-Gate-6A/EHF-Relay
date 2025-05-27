from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from sbdh_ubl_data.sbdh.standard_business_document_header import (
    StandardBusinessDocument,
)

def parse(message_text: str) -> StandardBusinessDocument:
    """Build object model from provided XML

    Args:
        message_text: the XML text to read
    """
    config = ParserConfig()
    context = XmlContext()
    parser = XmlParser(context=context, config=config)
    return parser.from_string(message_text)
