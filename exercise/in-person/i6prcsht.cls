\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{i6prcsht}[2014/04/16 i6 practice sheet]

% Process options
\newif\ifgerman
\DeclareOption{ngerman}{ % German strings
	\germantrue
	\PassOptionsToClass{\CurrentOption}{scrartcl}
	\PassOptionsToClass{\CurrentOption}{babel}
}
\DeclareOption{english}{
	\PassOptionsToClass{\CurrentOption}{babel}
}
\newif\ifSmallBorders
\DeclareOption{smallborders} { % Use small borders
	\SmallBorderstrue
}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrartcl}}
\ProcessOptions\relax

\LoadClass[a4paper,twoside=off,parskip=half]{scrartcl}

\RequirePackage{babel}
\RequirePackage[utf8]{inputenc} % Unicode is the only reasonable choice for the heterogeneous environment at LS6. UTF8 is the most common Unicode encoding.
\RequirePackage[T1]{fontenc} % Support for umlaute
\RequirePackage{lmodern} % Computer modern font with enhanced metrics and glyph coverage
\RequirePackageWithOptions{i6exc}    % Macros for semester, solution, ...
\RequirePackage{scrlayer-scrpage} % Customized footer
\RequirePackage{graphicx} % Include graphics for footer and title
\RequirePackage{lastpage} % Last page number for footer


%%% Macros for authors

% Use \lecture{long name}{abbreviation} to define name of lecture for title and footer
\newif\ifLectureDefined
\newcommand*{\lecture}[2]{\renewcommand{\LectureLong}{#1} \renewcommand{\LectureShort}{#2} \LectureDefinedtrue}


%%% Class-internal code

% Change border size if option smallborders was set
\ifSmallBorders
	\RequirePackage{geometry}
	\geometry{a4paper, top=20mm, left=25mm, right=25mm, bottom=25mm, headsep=10mm, footskip=10mm}
\fi

% Define commands for long and short lecture title
\newcommand{\LectureLong}{}
\newcommand{\LectureShort}{}

% Save title and subtitle for use in footer
% @title is cleared at some point (probably by \maketitle)
\newcommand*{\PracticeTitle}{}
\newcommand*{\OrigTitle}{}
\let\OrigTitle\title
\renewcommand*{\title}[1]{\OrigTitle{#1} \renewcommand*{\PracticeTitle}{#1}}
\newif\ifSubTitleDefined
\newcommand*{\PracticeSubTitle}{}
\newcommand*{\OrigSubTitle}{}
\let\OrigSubTitle\subtitle
\renewcommand*{\subtitle}[1]{\OrigSubTitle{#1} \renewcommand*{\PracticeSubTitle}{#1} \SubTitleDefinedtrue}

% Footer
\pagestyle{scrheadings}
\ifoot[]{\parbox{1cm}{\includegraphics[width=1cm]{i6prcsht_res/i6_icon}} \parbox{11cm}{\LectureShort,\ \semester* -- \PracticeTitle\ifSubTitleDefined \\ \fi \PracticeSubTitle}}
\cfoot[]{}
\ifgerman
	% \parbox is only necessary to achieve same vertical position of page number and one-line string in ifoot
	\ofoot[\parbox{3cm}{\begin{flushright}
				Seite \thepage\ von \pageref{LastPage}
			\end{flushright}}]{\parbox{3cm}{\begin{flushright}
				Seite \thepage\ von \pageref{LastPage}
			\end{flushright}}}
\else
	% \parbox is only necessary to achieve same vertical position of page number and one-line string in ifoot
	\ofoot[\parbox{3cm}{\begin{flushright}
				Page \thepage\ of \pageref{LastPage}
			\end{flushright}}]{\parbox{3cm}{\begin{flushright}
				Page \thepage\ of \pageref{LastPage}
			\end{flushright}}}
\fi

% Title
\titlehead{%
	\parbox[c]{4cm}{
		\includegraphics[width=4cm]{i6prcsht_res/fau_tech}
	}
	\hfill
	\parbox[c]{6cm}{
		\begin{center}
			\textsf{
				\textbf{\Department}\\
				\Chair
			}
		\end{center}
	}
	\hfill
	\parbox[c]{4cm}{
		\hfill % Graphic right aligned
		\includegraphics[width=2.6cm]{i6prcsht_res/i6_logo}
	}
}
\subject{\ifLectureDefined \LectureLong \\ \fi \semester}
\date{}
\author{}
