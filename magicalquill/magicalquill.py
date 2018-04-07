#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Decoupe les dossiers "dématérialisés" de Parcoursup pour avoir un fichier pdf par candidat.

E. Viennet 2014-04-12
J.-C. Dubacq 2015--2018
R. Lopez 2018-04
"""
import optparse
import os
import pdftotext

import PyPDF2


def main():
    """
    Point d'entrée pour le découpage de fichier.

    :return: codes de sortie standards.
    """
    # noinspection SpellCheckingInspection
    usage = 'usage: %prog [-o DIR] [-h] fichier'
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-h', '--help', action='help',
                      help="Affiche ce message d'aide et termine.")
    parser.add_option('-o', dest="outdir", help="Dossier de sortie des fichiers individuels", metavar="DIR",
                      default="output")
    (opt, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Mauvais nombre de paramètres.")

    input_pdf = args[0]
    outdir = opt.outdir

    print('Traitement de %s...' % input_pdf)

    with open(input_pdf, 'rb') as f:
        pdf = pdftotext.PDF(f, password='')
        nb_pages = len(pdf)
        print('%d pages' % nb_pages)
        pp = []  # indices de la premieres page de chaque dossier
        for p in range(0, nb_pages):
            if (p + 1) % 100 == 0:
                print('page %d...' % int(p + 1))
            page = pdf[p].lstrip().rstrip().split('\n')
            txt = page[0].split()
            if txt[0][:2] == 'N°' and txt[1][0] == 'M':
                nom = '_'.join(txt[2:])
                nom = nom.replace('_-', '-').replace('-_', '-').replace(' ', '_').replace('/', '-')
                code = txt[0].rstrip().lstrip('N°')
                if not nom or not code:
                    print('%s page %s *** invalid data !' % (input_pdf, p))
                oufilename = code + ' - ' + nom + '.pdf'
                pp.append((p, oufilename))

        print('%d candidats' % len(pp))

    with open(input_pdf, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)
        print('éclatement du pdf...')
        pp.append((nb_pages, None))
        if not (os.path.isdir(outdir)):
            os.mkdir(outdir)
        for i in range(len(pp) - 1):
            if i % 100 == 0:
                print('%d/%s (%s)' % (i + 1, len(pp) - 1, pp[i][1]))
            last_page = pp[i + 1][0]
            with open(outdir + '/' + pp[i][1], 'wb') as w:
                writer = PyPDF2.PdfFileWriter()
                for np in range(pp[i][0], last_page):
                    writer.addPage(pdf.getPage(np))
                writer.write(w)


if __name__ == '__main__':
    main()
