#!/usr/bin/env python3
"""
네이버 백과사전 검색 MCP 서버 실행 스크립트
"""

import sys
import os
import subprocess

def main():
    # 프로젝트 루트 디렉토리를 Python 경로에 추가
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 환경 변수에 PYTHONPATH 설정
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root
    
    # src/server.py 실행
    server_script = os.path.join(project_root, "src", "server.py")
    
    # 명령행 인수 전달
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    # 서브프로세스로 실행
    try:
        subprocess.run([sys.executable, server_script] + args, env=env, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n서버가 중단되었습니다.", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main() 