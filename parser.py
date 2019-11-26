# -*- coding: utf-8 -*-

from parser.cu import cu_parser
from parser.emart import emart_parser
from parser.gs25 import gs25_parser
from parser.seveneleven import seven_parser
from parser.ministop import ministop_parser


if __name__ == '__main__':
    # parser들 모아서 실행하는 코드
    cu_parser()
    emart_parser()
    gs25_parser()
    seven_parser()
    ministop_parser()
