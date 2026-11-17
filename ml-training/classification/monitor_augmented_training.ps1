# Monitor Augmented Model Training
# Run this script periodically to check training progress

$line = "=" * 70

Write-Host $line
Write-Host "AUGMENTED MODEL TRAINING MONITOR"
Write-Host $line

# Check for Python process
$pythonProcs = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like '*Apple_Leaf*'}
if ($pythonProcs) {
    Write-Host "`nSTATUS: RUNNING" -ForegroundColor Green
    foreach ($proc in $pythonProcs) {
        $runtime = ((Get-Date) - $proc.StartTime)
        Write-Host "  PID: $($proc.Id)"
        Write-Host "  Runtime: $($runtime.Hours)h $($runtime.Minutes)m $($runtime.Seconds)s"
        Write-Host "  Memory: $([math]::Round($proc.WS/1GB,2)) GB"
    }
} else {
    Write-Host "`nSTATUS: NOT RUNNING" -ForegroundColor Yellow
}

# Check for checkpoints
Write-Host "`nCHECKPOINTS:"
$checkpoints = Get-ChildItem ../checkpoints/*augmented*.pth -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending

if ($checkpoints) {
    foreach ($cp in $checkpoints) {
        $size = [math]::Round($cp.Length / 1MB, 2)
        Write-Host "  $($cp.Name)"
        Write-Host "    Size: $size MB, Modified: $($cp.LastWriteTime.ToString('HH:mm:ss'))"
    }
    
    # Read latest checkpoint
    Write-Host "`nLATEST CHECKPOINT INFO:"
    $latest = $checkpoints[0]
    python -c "import torch; cp = torch.load('../checkpoints/$($latest.Name)', map_location='cpu', weights_only=False); print(f'  Epoch: {cp[\"epoch\"]}'); print(f'  Validation Accuracy: {cp[\"val_acc\"]:.4f} ({cp[\"val_acc\"]*100:.2f}%)'); print(f'  Validation Loss: {cp[\"val_loss\"]:.4f}')"
    
} else {
    Write-Host "  (No checkpoints yet - first epoch not complete)"
}

# Training progress estimate
if ($pythonProcs -and $checkpoints) {
    Write-Host "`nTRAINING PROGRESS:"
    $latest = $checkpoints[0]
    python -c "
import torch
cp = torch.load('../checkpoints/$($latest.Name)', map_location='cpu', weights_only=False)
epoch = cp['epoch']
total_epochs = 50
progress = (epoch / total_epochs) * 100
print(f'  Completed: {epoch}/{total_epochs} epochs ({progress:.1f}%)')
print(f'  Best validation accuracy so far: {cp[\"val_acc\"]*100:.2f}%')
"
}

Write-Host "`n$line"
Write-Host "Run this script again to refresh status"
Write-Host $line
