"""Módulo da aplicação/projeto (projeto)."""

import os
import subprocess
import sys


# Função utilitária do projeto.
def venv_paths():
    if os.name == "nt":
        venv_python = os.path.join("venv", "Scripts", "python.exe")
        venv_pip = os.path.join("venv", "Scripts", "pip.exe")
    else:
        venv_python = os.path.join("venv", "bin", "python")
        venv_pip = os.path.join("venv", "bin", "pip")
    return venv_python, venv_pip


# Função utilitária do projeto.
def run_step(args, label, *, inherit_output=False):
    print(f"{label}... ", end="", flush=True)
    try:
        if inherit_output:
            subprocess.run(args, check=True)
            print("OK")
            return
        cp = subprocess.run(args, check=True, capture_output=True, text=True)
        print("OK")
        return cp
    except subprocess.CalledProcessError as e:
        print("ERRO")
        if getattr(e, 'stdout', None):
            print(e.stdout)
        if getattr(e, 'stderr', None):
            print(e.stderr, file=sys.stderr)
        raise


# Função utilitária do projeto.
def main():
    print("=== Configuração do Sistema de Posto de Combustível ===")

    # 1) Criar venv (se não existir)
    if not os.path.exists("venv"):
        run_step([sys.executable, "-m", "venv", "venv"], "Criando venv")

    venv_python, _ = venv_paths()

    # 2) Instalar dependências (sem upgrade de pip)
    run_step([venv_python, "-m", "pip", "install", "-r", "requirements.txt"], "Instalando dependências")

    # 3) Checar se há alterações em models sem migrations
    print("Verificando migrations pendentes... ", end="", flush=True)
    check = subprocess.run([venv_python, "manage.py", "makemigrations", "--check"], capture_output=True, text=True)
    if check.returncode != 0:
        print("PENDENTE")
        if check.stdout:
            print(check.stdout.strip())
        if check.stderr:
            print(check.stderr.strip(), file=sys.stderr)
        print("\nHá mudanças em models que não estão refletidas em migrations.")
        print("✅ Recomendado: criar a migration manualmente para versionar corretamente:\n   python manage.py makemigrations\n   python manage.py migrate")
        print("\n(Observação: gerar migrations automaticamente pode mascarar erro de versionamento; por isso este script apenas alerta.)")
        sys.exit(1)
    print("OK")

    # 4) Migrar
    run_step([venv_python, "manage.py", "migrate"], "Aplicando migrations", inherit_output=False)

    print("\n==================================================")
    print("CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("==================================================")
    if os.name == "nt":
        print("Para iniciar no Terminal:")
        print("  .\\venv\\Scripts\\Activate.ps1")
        print("  python manage.py runserver")
    else:
        print("Para iniciar:")
        print("  source venv/bin/activate")
        print("  python manage.py runserver")
    print("==================================================")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        sys.exit(1)
