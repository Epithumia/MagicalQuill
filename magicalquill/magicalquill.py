#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Découpe les dossiers "dématérialisés" de Parcoursup pour avoir un fichier pdf par candidat.

E. Viennet 2014-04-12
J.-C. Dubacq 2015--2018
R. Lopez 2018-2019
"""
import optparse
import os
import pdftotext

import PyPDF2


def vprint(str, verbose):
    if verbose:
        print(str)


def write_dossiers(input_pdf, indices, nb_pages, out_dir, opt):
    pp = indices['pp']
    pf = indices['pf']
    pfa = indices['pfa']
    pb = indices['pb']
    verbose = opt.verbose
    projet = opt.projet_pdf or opt.projet_texte
    fiche_avenir = opt.fiche_avenir
    bulletins = opt.bulletins
    with open(input_pdf, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)
        vprint('Eclatement du pdf...', verbose)
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
        vprint('Extraction des avis motivés...', verbose)
        for i in range(len(pf)):
            if opt.projet_pdf:
                if i % 100 == 0:
                    vprint('%d/%s (%s)' % (i + 1, len(pf) - 1, pf[i][1]), verbose)
                with open(out_dir + '/' + pf[i][1], 'wb') as w:
                    writer = PyPDF2.PdfFileWriter()
                    writer.addPage(pdf.getPage(pf[i][0]))
                    writer.write(w)
            if opt.projet_texte:
                f = pf[i][1].split('.pdf')[0] + '.txt'
                if i % 100 == 0:
                    vprint('%d/%s (%s)' % (i + 1, len(pf) - 1, f), verbose)
                with open(out_dir + '/' + f, 'w') as w:
                    w.write(pf[i][2])
    if fiche_avenir:
        vprint('Extraction des Fiches Avenir...', verbose)
        for i in range(len(pfa)):
            if i % 100 == 0:
                vprint('%d/%s (%s)' % (i + 1, len(pfa) - 1, pfa[i][1]), verbose)
            with open(out_dir + '/' + pfa[i][1], 'wb') as w:
                writer = PyPDF2.PdfFileWriter()
                writer.addPage(pdf.getPage(pfa[i][0]))
                writer.write(w)
    if bulletins:
        vprint('Extraction des bulletins...', verbose)
        for i in range(len(pb)):
            if i % 100 == 0:
                vprint('%d/%s (%s)' % (i + 1, len(pb) - 1, pb[i][2]), verbose)
            with open(out_dir + '/' + pb[i][2], 'wb') as w:
                writer = PyPDF2.PdfFileWriter()
                for p in range(pb[i][0], pb[i][1] + 1):
                    writer.addPage(pdf.getPage(p))
                writer.write(w)


def main():
    """
    Point d'entrée pour le découpage de fichier.

    :return: codes de sortie standards.
    """
    # noinspection SpellCheckingInspection
    usage = 'usage: %prog [-o DIR] [-p] [-t] [-v] [-h] fichier'
    parser = optparse.OptionParser(usage=usage, add_help_option=False)
    parser.add_option('-o', dest="outdir", help="Dossier de sortie des fichiers individuels.", metavar="DIR",
                      default="output")
    parser.add_option('-v', dest="verbose", action="store_true", default=False, help="Affiche la progression.")
    parser.add_option('-p', dest="projet_pdf", action="store_true", default=False,
                      help="Extrait les projets de formation au format pdf.")
    parser.add_option('-t', dest="projet_texte", action="store_true", default=False,
                      help="Extrait les projets de formation au format texte.")
    parser.add_option('-a', dest="fiche_avenir", action="store_true", default=False,
                      help="Extrait les Fiches Avenir au format pdf.")
    parser.add_option('-b', dest="bulletins", action="store_true", default=False,
                      help="Extrait les bulletins au format pdf.")
    parser.add_option('-h', '--help', action='help',
                      help="Affiche ce message d'aide et termine.")
    (opt, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Mauvais nombre de paramètres.")

    input_pdf = args[0]
    out_dir = opt.outdir
    verbose = opt.verbose
    projet = opt.projet_pdf or opt.projet_texte
    fiche_avenir = opt.fiche_avenir
    bulletins = opt.bulletins

    vprint('Traitement de %s...' % input_pdf, verbose)

    with open(input_pdf, 'rb') as f:
        pdf = pdftotext.PDF(f, password='')
        nb_pages = len(pdf)
        vprint('%d pages' % nb_pages, verbose)
        indices = {}
        pp = []  # indices de la premieres page de chaque dossier
        pf = []  # indices de la page du projet de formation motivé
        pfa = []  # indices de la page de la Fiche Avenir
        pb = []  # indices de la 1e page des bulletins
        out_filename = ''
        bu_filename = ''
        bulletin_start = False
        # Le hack ci-dessous est horrible. On détecte la fin de la section des bulletins
        # en cherchant la ligne horizontale qui nest pas en bas de page
        bulletin_end = '_____________________________________________________________________________________________________________________________'
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
                pfm = '\n'.join(page[7:-1])
                pf.append((p, pf_filename, pfm))
            if fiche_avenir and txt[0] == 'Appréciations' and txt[2] == 'professeurs':
                fa_filename = out_filename.split('.pdf')[0] + ' - Fiche_Avenir.pdf'
                pfa.append((p, fa_filename))
            if bulletins and txt[0] == 'Bulletins' and txt[1] == 'scolaires' and not bulletin_start:
                bu_filename = out_filename.split('.pdf')[0] + ' - Bulletins.pdf'
                bulletin_start = p
            if bulletin_start and bulletin_end in page[:-1]:
                pb.append((bulletin_start, p, bu_filename))
                bulletin_start = False

        vprint('%d candidats' % len(pp), verbose)
        indices['pp'] = pp
        indices['pf'] = pf
        indices['pfa'] = pfa
        indices['pb'] = pb

    write_dossiers(input_pdf, indices, nb_pages, out_dir, opt)


if __name__ == '__main__':
    main()
