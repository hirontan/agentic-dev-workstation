# Bash用。既存PATHとの重複を避ける。
case ":$PATH:" in
    *":$HOME/.local/bin:"*) ;;
    *) export PATH="$HOME/.local/bin:$PATH" ;;
esac
# direnvは任意。プロジェクト内容を確認してからdirenv allowする。
# command -v direnv >/dev/null && eval "$(direnv hook bash)"
