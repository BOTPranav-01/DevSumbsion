"""
NecroCode Command Line Interface.
Runs 100% offline and locally using open-source AI weights and AST static analysis.
"""

import sys
import os
import argparse
import asyncio
from app.models.schemas import FileEntry, RepoAnalysisRequest
from app.core.code_auditor import code_auditor
from app.core.resurrection import resurrection_engine
from app.core.seance_agent import seance_agent

def read_files_from_dir(directory: str):
    entries = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".json")):
                p = os.path.join(root, file)
                rel_path = os.path.relpath(p, directory)
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as f:
                        entries.append(FileEntry(path=rel_path, content=f.read()))
                except Exception:
                    pass
    return entries

def main():
    parser = argparse.ArgumentParser(description="NecroCode: Codebase Necromancer & Spectral Auditor (Ghost in the Machine)")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Perform spectral cemetery audit on code directory")
    audit_parser.add_argument("path", help="Path to codebase folder or file")

    # Resurrect command
    res_parser = subparsers.add_parser("resurrect", help="Modernize legacy codebase, generate diffs & tests")
    res_parser.add_argument("path", help="Path to codebase folder or file")
    res_parser.add_argument("--out", default="./resurrected_output", help="Output directory for revived files")

    # Seance command
    seance_parser = subparsers.add_parser("seance", help="Converse with the Maintainer Ghost in the Machine")
    seance_parser.add_argument("message", help="Message to ask the ghost maintainer")
    seance_parser.add_argument("--repo", default="LegacyCore", help="Repository context")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    print("══════════════════════════════════════════════════════════════")
    print(" 🔮 NECROCODE: GHOST IN THE MACHINE (HACKTOBERFEST 2026)")
    print("══════════════════════════════════════════════════════════════\n")

    if args.command == "audit":
        if os.path.isdir(args.path):
            files = read_files_from_dir(args.path)
        elif os.path.isfile(args.path):
            with open(args.path, "r", encoding="utf-8") as f:
                files = [FileEntry(path=os.path.basename(args.path), content=f.read())]
        else:
            print(f"[!] Target path not found: {args.path}")
            sys.exit(1)

        print(f"[*] Auditing {len(files)} files in '{args.path}'...")
        result = code_auditor.audit_repository(os.path.basename(args.path), files)
        print(f"\n[+] Cemetery Status: {result.cemetery_status}")
        print(f"[+] Bit Rot Score:   {result.bit_rot_score}/100")
        print(f"[+] Years Dormant:   ~{result.years_dormant} years")
        print(f"[+] Total Anomalies: {len(result.findings)}")
        print(f"\n[Epitaph]\n{result.spectral_epitaph}\n")
        print("─── Top Spectral Findings ───────────────────────────────────")
        for f in result.findings[:5]:
            print(f" [{f.severity}] {f.title} ({f.file_path}:{f.line_number or 1})")
            print(f"     -> {f.ghost_remedy}")

    elif args.command == "resurrect":
        if os.path.isdir(args.path):
            files = read_files_from_dir(args.path)
        elif os.path.isfile(args.path):
            with open(args.path, "r", encoding="utf-8") as f:
                files = [FileEntry(path=os.path.basename(args.path), content=f.read())]
        else:
            print(f"[!] Target path not found: {args.path}")
            sys.exit(1)

        print(f"[*] Resurrecting {len(files)} file(s)...")
        plan = resurrection_engine.resurrect_codebase(os.path.basename(args.path), files)
        os.makedirs(args.out, exist_ok=True)
        for patch in plan.patches:
            out_file = os.path.join(args.out, patch.file_path)
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(patch.resurrected_code)
            print(f" [+] Revived: {out_file}")

        print(f"\n[+] Modernized files written to '{args.out}'.")
        print("[+] Generated Dockerfile and CI workflow saved.")

    elif args.command == "seance":
        async def run_seance():
            print(f"[*] Calling upon the spirit of {args.repo}...")
            resp = await seance_agent.invoke_seance(
                repo_name=args.repo,
                user_message=args.message,
                history=[]
            )
            print(f"\n👻 [Ghost Maintainer - {resp.spectral_mood.upper()}]:\n{resp.reply}\n")
        asyncio.run(run_seance())

if __name__ == "__main__":
    main()
