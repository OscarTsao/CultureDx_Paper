from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

COLORS={"panel":"#F7F7F7","input":"#E8F3E8","llm":"#FCE8D6","det":"#E8E0F4","artifact":"#FFFFFF","final":"#DDEFF0","missing":"#FFF4CC","ink":"#202020","muted":"#666666"}

def box(ax,x,y,w,h,text,face="artifact",edge="ink",linewidth=1.4,linestyle="-",fontsize=9.2,weight="normal",align="center",pad=.009,zorder=2):
    p=FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad={pad},rounding_size=0.012",facecolor=COLORS.get(face,face),edgecolor=COLORS.get(edge,edge),linewidth=linewidth,linestyle=linestyle,zorder=zorder)
    ax.add_patch(p)
    ha=align
    tx=x+w/2 if align=="center" else x+.018
    ax.text(tx,y+h/2,text,ha=ha,va="center",fontsize=fontsize,fontweight=weight,color=COLORS['ink'],linespacing=1.20,zorder=zorder+1)
    return p

def arrow(ax,start,end,dashed=False,color="ink",linewidth=1.3,mutation_scale=12,zorder=3,rad=0):
    a=FancyArrowPatch(start,end,arrowstyle="-|>",mutation_scale=mutation_scale,linewidth=linewidth,linestyle="--" if dashed else "-",color=COLORS.get(color,color),shrinkA=2,shrinkB=2,zorder=zorder,connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a); return a

def save(fig, path: Path) -> None:
    fig.savefig(path,bbox_inches='tight',metadata={'CreationDate':None,'ModDate':None}); plt.close(fig)

def make_single_vs_hied(path: Path) -> None:
    fig,ax=plt.subplots(figsize=(13.5,7.6)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    box(ax,.02,.035,.32,.92,"",face='panel',linewidth=1.2,zorder=0)
    box(ax,.37,.035,.61,.92,"",face='panel',linewidth=1.2,zorder=0)
    ax.text(.045,.91,'A. Single LLM baseline',fontsize=13.2,fontweight='bold',va='top')
    ax.text(.395,.91,'B. HiED two-path architecture',fontsize=13.2,fontweight='bold',va='top')
    box(ax,.08,.75,.20,.085,'Fixed transcript',face='input',weight='bold')
    box(ax,.08,.62,.20,.075,'Optional similar cases',linestyle='--',fontsize=8.8)
    box(ax,.095,.43,.17,.11,'Single LLM',face='llm',weight='bold',fontsize=11)
    box(ax,.055,.19,.25,.15,'Recorded final outputs\n\nPrimary diagnosis\nOptional emitted labels',linestyle='--',weight='bold',fontsize=9.0)
    arrow(ax,(.18,.75),(.18,.54)); arrow(ax,(.18,.62),(.18,.54),dashed=True); arrow(ax,(.18,.43),(.18,.34))
    ax.text(.18,.12,'No standardized ranked differential or\ndiagnosis-specific criterion record\nunder the evaluated output contract',ha='center',va='center',fontsize=8.1,color=COLORS['muted'],style='italic',linespacing=1.2)
    box(ax,.56,.77,.22,.075,'Fixed transcript',face='input',weight='bold')
    box(ax,.39,.66,.18,.065,'Optional similar cases',linestyle='--',fontsize=8.4)
    box(ax,.41,.49,.20,.12,'Diagnosis path\n\nDiagnostician',face='llm',weight='bold',fontsize=9.8)
    box(ax,.70,.47,.23,.14,'Criterion-checking path\n\nDiagnosis-specific\nCriterion Checkers\n\nAll 14 configured categories',face='llm',weight='bold',fontsize=8.2)
    box(ax,.39,.27,.24,.17,'Recorded diagnosis outputs\n\nRanked candidates (up to 5)\nProposed primary\nOptional comorbid diagnosis',linestyle='--',weight='bold',fontsize=8.6)
    box(ax,.69,.30,.25,.12,'Criterion states\n\nmet  |  not_met\ninsufficient_evidence',linestyle='--',weight='bold',fontsize=8.6)
    box(ax,.72,.19,.20,.07,'Compatibility Auditor',face='det',linewidth=2.0,weight='bold',fontsize=8.9)
    box(ax,.70,.105,.24,.055,'Criterion-compatible set',linestyle='--',weight='bold',fontsize=8.5)
    box(ax,.43,.13,.19,.075,'Finalization policy\nDA or NtS',face='det',linewidth=2.0,weight='bold',fontsize=8.8)
    box(ax,.40,.052,.25,.05,'Committed primary diagnosis',face='final',linewidth=2.4,weight='bold',fontsize=8.5)
    arrow(ax,(.64,.77),(.51,.61)); arrow(ax,(.70,.77),(.815,.61)); arrow(ax,(.48,.66),(.46,.61),dashed=True)
    arrow(ax,(.51,.49),(.51,.44)); arrow(ax,(.815,.47),(.815,.42)); arrow(ax,(.815,.30),(.815,.26)); arrow(ax,(.82,.19),(.82,.16))
    arrow(ax,(.51,.27),(.52,.205)); arrow(ax,(.70,.132),(.62,.167),rad=.08); arrow(ax,(.525,.13),(.525,.102))
    save(fig,path)

def make_worked_example(path: Path) -> None:
    fig,ax=plt.subplots(figsize=(12.5,10.5)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    box(ax,.14,.90,.72,.07,'Complete constructed transcript\nIllustrative case - not a patient record or exported model trace',face='input',linewidth=1.8,weight='bold',fontsize=10)
    box(ax,.13,.72,.24,.105,'Diagnosis path\n\nDiagnostician',face='llm',weight='bold',fontsize=9.7)
    box(ax,.05,.48,.40,.20,'Illustrative ranked candidates\n\n1. F41.1 Generalized anxiety disorder\n2. F32 Depressive episode\n3. F51 Nonorganic sleep disorder\n\nProposed primary: F41.1\nOptional comorbidity: None',linestyle='--',weight='bold',fontsize=8.5,align='left')
    ax.text(.25,.455,'Up to five candidates may be retained; only the leading three are shown.',ha='center',va='top',fontsize=7.6,color=COLORS['muted'],style='italic')
    box(ax,.63,.71,.26,.115,'Criterion-checking path\n\nDiagnosis-specific Criterion Checkers\nAll 14 categories checked',face='llm',weight='bold',fontsize=8.4)
    box(ax,.50,.56,.21,.13,'F32\n\nCore symptoms: met\nDuration: met\nAssociated symptoms: met\n\nIncluded',linestyle='--',weight='bold',fontsize=7.9,align='left')
    box(ax,.75,.53,.22,.16,'F41.1\n\nMulti-area worry: met\nRequired duration:\ninsufficient_evidence\nAssociated symptoms:\ninsufficient_evidence\n\nNot included',linestyle='--',weight='bold',fontsize=7.4,align='left')
    box(ax,.61,.39,.26,.10,'F31\n\nPrevious manic episode: not_met\n\nNot included',linestyle='--',weight='bold',fontsize=7.9,align='left')
    box(ax,.64,.285,.24,.065,'Compatibility Auditor',face='det',linewidth=2.0,weight='bold',fontsize=8.8)
    box(ax,.67,.215,.18,.045,'Compatible set: {F32}',linestyle='--',weight='bold',fontsize=8.2)
    arrow(ax,(.43,.90),(.25,.825)); arrow(ax,(.57,.90),(.76,.825)); arrow(ax,(.25,.72),(.25,.68))
    arrow(ax,(.76,.71),(.605,.69),rad=.05); arrow(ax,(.76,.71),(.86,.69),rad=-.04); arrow(ax,(.76,.71),(.74,.49),rad=0)
    arrow(ax,(.74,.39),(.76,.35)); arrow(ax,(.76,.285),(.76,.26))
    box(ax,.06,.085,.38,.10,'Direct-Answer\n\nKeep the proposed primary\nCommitted primary: F41.1',face='final',linewidth=2.2,weight='bold',fontsize=9.0)
    box(ax,.56,.085,.38,.10,'Nominate-then-Select\n\nChoose the highest-ranked compatible candidate\nCommitted primary: F32',face='final',linewidth=2.2,weight='bold',fontsize=8.7)
    arrow(ax,(.25,.48),(.25,.185)); arrow(ax,(.45,.52),(.67,.185),rad=-.12); arrow(ax,(.76,.215),(.75,.185))
    box(ax,.20,.012,.60,.05,'Important missing information\nOnset and duration of the anxiety symptoms remain unclear',face='missing',linestyle=':',linewidth=2.0,weight='bold',fontsize=9.0)
    save(fig,path)

def main() -> None:
    if Path("school/main.tex").exists():
        out_dir = Path("figures")
    elif Path("paper/school/HiED_school_version.tex").exists():
        out_dir = Path("paper/figures")
    else:
        raise FileNotFoundError("Could not identify the School thesis repository layout")

    make_single_vs_hied(out_dir / "fig_single_vs_hied_architecture.pdf")
    make_worked_example(out_dir / "fig_worked_example_flow.pdf")
    print(f"Generated Chapter 3 figures in {out_dir}")


if __name__ == "__main__":
    main()
