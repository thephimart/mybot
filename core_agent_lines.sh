#!/bin/bash
# Count core agent lines (excluding channels/, cli/, providers/)
# agent/ is reported WITHOUT agent/tools/, which is shown separately

cd "$(dirname "$0")" || exit 1

echo "mybot core agent line count"
echo "================================"
echo ""

# --- agent/tools ---
agent_tools=$(find mybot/agent/tools -name "*.py" -type f -exec cat {} + | wc -l)

# --- agent/ excluding tools ---
agent_total=$(find mybot/agent -name "*.py" -type f ! -path "*/tools/*" -exec cat {} + | wc -l)

printf "  %-16s %5s lines\n" "agent/" "$agent_total"
printf "    %-14s %5s lines\n" "tools/" "$agent_tools"

# --- other core dirs ---
for dir in bus config cron heartbeat session utils; do
  count=$(find "mybot/$dir" -name "*.py" -type f -exec cat {} + | wc -l)
  printf "  %-16s %5s lines\n" "$dir/" "$count"
done

# --- root files ---
root=$(find mybot -maxdepth 1 -name "*.py" -type f -exec cat {} + | wc -l)
printf "  %-16s %5s lines\n" "(root)" "$root"

echo ""

# --- subtotal ---
subtotal=$((agent_total + agent_tools + root))
for dir in bus config cron heartbeat session utils; do
  count=$(find "mybot/$dir" -name "*.py" -type f -exec cat {} + | wc -l)
  subtotal=$((subtotal + count))
done
echo "  Core subtotal:  $subtotal lines"

# --- authoritative total ---
total=$(find mybot -name "*.py" \
  ! -path "*/channels/*" \
  ! -path "*/cli/*" \
  ! -path "*/providers/*" \
  -exec cat {} + | wc -l)

echo "  Core total:     $total lines"
echo ""
echo "  (excludes: channels/, cli/, providers/)"

# --- sanity check ---
if [ "$subtotal" -ne "$total" ]; then
  echo ""
  echo "⚠️  WARNING: Subtotal and authoritative total differ."
  echo "   This usually means a new directory was added to mybot/"
  echo "   and should be classified as core or excluded."
fi
