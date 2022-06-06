from __future__ import division

import math
import os

import six
from django.conf import settings
from fpdf import FPDF


class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super(PDF, self).__init__(*args, **kwargs)
        font_family = 'Times New Roman'
        font_folder = os.path.join(settings.BASE_DIR, 'fonts', 'times_new_roman')
        self.add_font(font_family, '', os.path.join(font_folder, 'times.ttf'), True)
        self.add_font(font_family, 'B', os.path.join(font_folder, 'timesbd.ttf'), True)
        self.add_font(font_family, 'BI', os.path.join(font_folder, 'timesbi.ttf'), True)
        self.add_font(font_family, 'I', os.path.join(font_folder, 'timesi.ttf'), True)
        self.set_font(font_family)
        self.alias_nb_pages()

    def set_font_style(self, style=''):
        self.set_font('', style)

    def footer(self):
        if self.b_margin > 0:
            self.set_font_style()
            self.set_y(self.page_break_trigger)
            self.cell(0, self.b_margin, 'Trang %d / {nb}' % self.page, 0, 0, 'C')

    def get_xy(self):
        return self.get_x(), self.get_y()

    def writeln(self, h, txt='', style='', ln=0, link=''):
        self.set_font_style(style)
        x = self.get_x()
        self.write(h, txt, link)
        if ln == 1:
            self.ln(h)
        elif ln == 2:
            self.set_xy(x, self.get_y() + h)

    def multi_cell_vertical_center(self, w, h, n, m, txt='', border=0, ln=0, align='L', fill=0, link=''):
        """
        Write multi_cell in vertical-center
        :param n: number of total rows
        :param m: number of actual rows
        """
        x, y = self.x, self.y
        self.cell(w, h * n, border=border, ln=ln, fill=fill, link=link)
        _xy = self.get_xy()
        self.set_xy(x, y + h * (n - m) / 2)
        self.multi_cell(w, h, txt, align=align)
        self.set_xy(*_xy)

    def calculate_strings_width(self, strings):
        if isinstance(strings, six.string_types):
            strings = [strings]
        w = max(map(self.get_string_width, strings)) + 2 * self.c_margin
        w = math.ceil(w * 100) / 100
        return w

    @property
    def inner_w(self):
        # inner width
        return self.w - self.l_margin - self.r_margin

    def multi_cell_get_height(self, w, h, txt='', border=0, align='J', fill=0, split_only=False):
        "Output text with automatic or explicit line breaks"
        txt = self.normalize_text(txt)
        ret = [] # if split_only = True, returns splited text cells
        cw=self.current_font['cw']
        if(w==0):
            w=self.w-self.r_margin-self.x
        wmax=(w-2*self.c_margin)*1000.0/self.font_size
        s=txt.replace("\r",'')
        nb=len(s)
        if(nb>0 and s[nb-1]=="\n"):
            nb-=1
        b=0
        if(border):
            if(border==1):
                border='LTRB'
                b='LRT'
                b2='LR'
            else:
                b2=''
                if('L' in border):
                    b2+='L'
                if('R' in border):
                    b2+='R'
                if ('T' in border):
                    b=b2+'T'
                else:
                    b=b2
        sep=-1
        i=0
        j=0
        l=0
        ns=0
        nl=1
        while(i<nb):
            #Get next character
            c=s[i]
            if(c=="\n"):
                #Explicit line break
                if(self.ws>0):
                    self.ws=0
                    if not split_only:
                        self._out('0 Tw')
                if not split_only:
                    self.cell(w,h,s[j,i-j],b,2,align,fill)
                else:
                    ret.append(s[j,i-j])
                i+=1
                sep=-1
                j=i
                l=0
                ns=0
                nl+=1
                if(border and nl==2):
                    b=b2
                continue
            if(c==' '):
                sep=i
                ls=l
                ns+=1
            if self.unifontsubset:
                l += self.get_string_width(c) / self.font_size*1000.0
            else:
                l += cw.get(c,0)
            if(l>wmax):
                #Automatic line break
                if(sep==-1):
                    if(i==j):
                        i+=1
                    if(self.ws>0):
                        self.ws=0
                        if not split_only:
                            self._out('0 Tw')
                    if not split_only:
                        self.cell(w,h,s[j,i-j],b,2,align,fill)
                    else:
                        ret.append(s[j,i-j])
                else:
                    if(align=='J'):
                        if ns>1:
                            self.ws=(wmax-ls)/1000.0*self.font_size/(ns-1)
                        else:
                            self.ws=0
                        if not split_only:
                            self._out('%.3f Tw'%self.ws*self.k)
                    if not split_only:
                        self.cell(w,h,s[j,sep-j],b,2,align,fill)
                    else:
                        ret.append(s[j,sep-j])
                    i=sep+1
                sep=-1
                j=i
                l=0
                ns=0
                nl+=1
                if(border and nl==2):
                    b=b2
            else:
                i+=1
        #Last chunk
        if(self.ws>0):
            self.ws=0
            if not split_only:
                self._out('0 Tw')
        if(border and 'B' in border):
            b+='B'
        if not split_only:
            self.cell(w,h,s[j,i-j],b,2,align,fill)
            self.x=self.l_margin
        else:
            ret.append(s[j,i-j])
        return nl