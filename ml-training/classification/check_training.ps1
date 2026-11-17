# Training Monitor Script
param([int]$ProcessId = 22072)

$line = "=" * 70
Write-Host $line
Write-Host "DENSENET121 TRAINING MONITOR"
Write-Host $line

# Check if process is running
$process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue

if ($process) {
    $runtime = ((Get-Date) - $process.StartTime)
    $cpu = [math]::Round($process.CPU, 2)
    $memory_gb = [math]::Round($process.WS / 1GB, 2)
    
    Write-Host ""
    Write-Host "STATUS: RUNNING" -ForegroundColor Green
    Write-Host "   Process ID: $($process.Id)"
    Write-Host "   Runtime: $($runtime.Hours)h $($runtime.Minutes)m $($runtime.Seconds)s"
    Write-Host "   CPU Time: $cpu seconds"
    Write-Host "   Memory: $memory_gb GB"
} else {
    Write-Host ""
    Write-Host "STATUS: NOT RUNNING" -ForegroundColor Red
}

# Check for checkpoints
Write-Host ""
Write-Host "CHECKPOINTS:"
$checkpoints = Get-ChildItem "g:\Apple_Leaf\ml-training\checkpoints\*.pth" -ErrorAction SilentlyContinue
if ($checkpoints) {
    foreach ($cp in $checkpoints) {
        $size_mb = [math]::Round($cp.Length / 1MB, 2)
        Write-Host "   $($cp.Name) ($size_mb MB) - $($cp.LastWriteTime.ToString('HH:mm:ss'))"
    }
} else {
    Write-Host "   (No checkpoints yet)"
}

# Check training history
Write-Host ""
Write-Host "TRAINING HISTORY:"
$history_file = "g:\Apple_Leaf\ml-training\reports\training_history.json"
if (Test-Path $history_file) {
    $history = Get-Content $history_file | ConvertFrom-Json
    $epochs_completed = $history.train_loss.Count
    
    Write-Host "   Epochs Completed: $epochs_completed / 50"
    
    if ($epochs_completed -gt 0) {
        $latest_idx = $epochs_completed - 1
        Write-Host ""
        Write-Host "   Latest Epoch:"
        Write-Host "      Train Loss: $([math]::Round($history.train_loss[$latest_idx], 4))"
        Write-Host "      Train Acc:  $([math]::Round($history.train_acc[$latest_idx], 4))"
        Write-Host "      Val Loss:   $([math]::Round($history.val_loss[$latest_idx], 4))"
        Write-Host "      Val Acc:    $([math]::Round($history.val_acc[$latest_idx], 4))"
        
        # Find best
        $best_val_acc = ($history.val_acc | Measure-Object -Maximum).Maximum
        Write-Host ""
        Write-Host "   Best Val Acc: $([math]::Round($best_val_acc, 4))"
    }
} else {
    Write-Host "   (No history yet)"
}

Write-Host ""
Write-Host $line
