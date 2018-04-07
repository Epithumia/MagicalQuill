#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Découpe les dossiers "dématérialisés" de Parcoursup pour avoir un fichier pdf par candidat.

E. Viennet 2014-04-12
J.-C. Dubacq 2015--2018
R. Lopez 2018-04
"""
import optparse
import os
import pdftotext

import PyPDF2


def vprint(str, verbose):
    if verbose:
        print(str)


def write_dossiers(input_pdf, pp, pf, nb_pages, out_dir, verbose, projet):
    with open(input_pdf, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)
        vprint('éclatement du pdf...', verbose)
        pp.append((nb_pages, None))
        if not (os.path.isdir(out_dir)):
            os.mkdir(out_dir)
        for i in range(len(pp) - 1):
            if i % 100 == 0:
                vprint('%d/%s (%s)' % (i + 1, len(pp) - 1, pp[i][1]), verbose)
            last_page = pp[i + 1][0]
            with open(out_dir + '/' + pp[i][1], 'wb') as w:
                writer = PyPDF2.PdfFileWriter()
                for np in range(pp[i][0], last_page):
                    writer.addPage(pdf.getPage(np))
                writer.write(w)
    if projet:
        for i in range(len(pf)):
            if i % 100 == 0:
                vprint('%d/%s (%s)' % (i + 1, len(pf) - 1, pf[i][1]), verbose)
            with open(out_dir + '/' + pf[i][1], 'wb') as w:
                writer = PyPDF2.PdfFileWriter()
                writer.addPage(pdf.getPage(pf[i][0]))
                writer.write(w)


def main():
    """
    Point d'entrée pour le découpage de fichier.

    :return: codes de sortie standards.
    """
    # noinspection SpellCheckingInspection
    usage = 'usage: %prog [-o DIR] [-h] fichier'
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-o', dest="outdir", help="Dossier de sortie des fichiers individuels.", metavar="DIR",
                      default="output")
    parser.add_option('-v', dest="verbose", action="store_true", default=False, help="Affiche la progression.")
    parser.add_option('-p', dest="projet", action="store_true", default=False, help="Extrait les projets de formation.")
    parser.add_option('-h', '--help', action='help',
                      help="Affiche ce message d'aide et termine.")
    (opt, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Mauvais nombre de paramètres.")

    input_pdf = args[0]
    outdir = opt.outdir
    verbose = opt.verbose
    projet = opt.projet

    vprint('Traitement de %s...' % input_pdf, verbose)

    with open(input_pdf, 'rb') as f:
        pdf = pdftotext.PDF(f, password='')
        nb_pages = len(pdf)
        vprint('%d pages' % nb_pages, verbose)
        pp = []  # indices de la premieres page de chaque dossier
        pf = []  # indices de la page du projet de formation motivé
        out_filename = ''
        for p in range(0, nb_pages):
            if (p + 1) % 100 == 0:
                vprint('page %d...' % int(p + 1), verbose)
            page = pdf[p].lstrip().rstrip().split('\n')
            txt = page[0].split()
            if txt[0][:2] == 'N°' and txt[1][0] == 'M':
                nom = '_'.join(txt[2:])
                nom = nom.replace('_-', '-').replace('-_', '-').replace(' ', '_').replace('/', '-')
                code = txt[0].rstrip().lstrip('N°')
                if not nom or not code:
                    print('%s page %s *** invalid data !' % (input_pdf, p))
                out_filename = code + ' - ' + nom + '.pdf'
                pp.append((p, out_filename))
            if projet and txt[0] == 'Projet' and txt[2] == 'formation' and txt[3] == 'motivé':
                pf_filename = out_filename.split('.pdf')[0] + ' - Projet_Formation.pdf'
                pfm = '\n'.join(page[7:-4])
                pf.append((p, pf_filename, pfm))
        vprint('%d candidats' % len(pp), verbose)

    write_dossiers(input_pdf, pp, pf, nb_pages, outdir, verbose, projet)


if __name__ == '__main__':
    main()
