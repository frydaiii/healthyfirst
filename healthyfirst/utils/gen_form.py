#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
import logging

from datetime import datetime
from healthyfirst.api.models import Premise, Certificate
from healthyfirst.api.serializers import PremiseSerializer, CertificateSerializer

from healthyfirst.utils.pdf import PDF

logger = logging.getLogger('main')
A4_WIDTH = 210


class GenForm:
    help = "Generate information collection form after registration"

    FILE_NAME_PATTERN = 'chung_nhan_%s.pdf'
    FONT_SIZE = 14
    MARGIN_TOP, MARGIN_LEFT = 20, 20
    LINE_WIDTH = A4_WIDTH - MARGIN_LEFT * 2

    def __init__(self, cert_id):
        # super(Command, self).__init__()
        self.pdf = None
        self.file_name = self.FILE_NAME_PATTERN % (datetime.now().strftime('%d%m%Y_%H%M%S'))
        self.local_path = os.path.abspath(os.getcwd())
        self.cert_id = cert_id

    def gen_file(self):
            if not os.path.exists(self.local_path):
                os.makedirs(self.local_path)

            self.init_pdf_file()

            premise = PremiseSerializer(Premise.objects.filter(id_certificate=self.cert_id).first())
            cert = CertificateSerializer(Certificate.objects.get(id=self.cert_id))

            data = {
                'premise': premise.data,
                'certificate': cert.data,
            }
            self.write_form(data)

            path = os.path.join(self.local_path, 'certificates', self.file_name)

            self.pdf.output(path, 'F')

            return path

    def write_form(self, data):
        pdf = self.pdf
        h = 7.5
        empty_date = '....../....../..........'
        endline_x = A4_WIDTH - self.MARGIN_LEFT
        middle_x = A4_WIDTH / 2
        pdf.add_page()
        pdf.set_font_style('B')
        pdf.cell(0, h=h, txt=u'CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM', ln=1, align='C')
        pdf.cell(0, h=h, txt=u'Độc lập - Tự do - Hạnh phúc', ln=1, align='C')

        pdf.set_font_style()
        pdf.cell(0, h=4, txt=u'-' * 20, ln=1, align='C')
        pdf.ln(4)

        pdf.set_font_style('B')
        pdf.cell(0, h=h, txt=u'GIẤY CHỨNG NHẬN AN TOÀN VỆ SINH THỰC PHẨM', ln=1, align='C')
        pdf.ln(4)
        pdf.cell(0, h=h, txt=u'I. Thông tin cơ sở:', ln=1)
        pdf.set_font_style()

        pdf.write(h, txt=u'Tên cơ sở:  ')
        if data['premise']['name']:
            pdf.set_font_style('B')
            pdf.cell(0, h=h, txt=str(data['premise']['name']), ln=1)
            pdf.set_font_style()
        else:
            pdf.cell(0, h=h, txt=self.filled_with_dots(' ', endline_x - pdf.x), ln=1, align='R')


        pdf.write(h, txt=u'Địa chỉ: ')
        if data['premise']['address'] == '':
            pdf.cell(0, h=h, txt=self.filled_with_dots(' ', endline_x - pdf.x), ln=1, align='R')
        else:
            pdf.set_font_style('B')
            pdf.write(h, txt=data['premise']['address'])
            pdf.set_font_style()
            pdf.ln(h)

        pdf.set_font_style('B')
        pdf.cell(0, h=h, txt=u'II. Thông tin điều chỉnh/bổ sung (nếu có):', ln=1)
        pdf.set_font_style()

        pdf.cell(0, h=h, txt=u'I. Thông tin chứng nhận:', ln=1)
        pdf.set_font_style()

        pdf.write(h, txt=u'Ngày cấp: ' + data['certificate']['issued_date'])
        pdf.cell(0, h=h, txt=self.filled_with_dots(' ', endline_x - pdf.x), ln=1, align='R')
        pdf.write(h, txt=u'Số: ' + data['certificate']['series'])
        pdf.cell(0, h=h, txt=self.filled_with_dots(' ', endline_x - pdf.x), ln=1, align='R')
        pdf.write(h, txt=u'Hiệu lực đến: ' + data['certificate']['expired_date'])
        pdf.cell(0, h=h, txt=self.filled_with_dots(' ', endline_x - pdf.x), ln=1, align='R')


        pdf.cell(0, h=h, txt=u'Tôi xác nhận cơ sở đủ điều kiện vệ sinh an toàn thực phẩm.', ln=1)

        pdf.ln(4)
        pdf.x = 120
        pdf.cell(50, h=h, txt=u'..........., ngày ..... tháng ..... năm .....', ln=1, align='C')

        pdf.set_font_style('B')
        pdf.x = 120
        pdf.cell(50, h=h, txt=u'Người cấp', ln=1, align='C')
        pdf.set_font_style()

        pdf.set_font_style('I')
        pdf.x = 120
        pdf.cell(50, h=h, txt=u'(Ký, ghi rõ họ tên)', ln=1, align='C')
        pdf.set_font_style()

    def filled_with_dots(self, s, w):
        length = self.pdf.get_string_width(s)
        dot_length = self.pdf.get_string_width(u'.')
        max_length = w
        num_dots = int((max_length - length) / dot_length)
        return s + u'.' * num_dots

    def init_pdf_file(self):
        self.pdf = PDF()
        self.pdf.set_margins(self.MARGIN_LEFT, self.MARGIN_TOP)
        self.pdf.set_auto_page_break(False)
        self.pdf.set_font_size(self.FONT_SIZE)

