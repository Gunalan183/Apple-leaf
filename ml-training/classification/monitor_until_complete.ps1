# Continuous Training Monitor - Checks until training completes
param(
    [int]$ProcessId = 22072,
    [int]$CheckIntervalSeconds = 300  # Check every 5 minutes
)

$lastEpoch = 0
$noChangeCount = 0
$checkpointPath = "g:\Apple_Leaf\ml-training\checkpoints\densenet121_latest.pth"

Write-Host "=" * 70
Write-Host "CONTINUOUS TRAINING MONITOR"
Write-Host "=" * 70
Write-Host "Process ID: $ProcessId"
Write-Host "Check Interval: $CheckIntervalSeconds seconds ($([math]::Round($CheckIntervalSeconds/60, 1)) minutes)"
Write-Host "Started: $(Get-Date -Format 'HH:mm:ss')"
Write-Host "=" * 70

while ($true) {
    Start-Sleep -Seconds $CheckIntervalSeconds
    
    $timestamp = Get-Date -Format 'HH:mm:ss'
    Write-Host "`n[$timestamp] Checking status..."
    
    # Check if process is still running
    $process = Get-Process -Id $ProcessId -ErrorAction SilentlyContinue
    
    if (-not $process) {
        Write-Host "`n" + ("=" * 70)
        Write-Host "TRAINING COMPLETED!" -ForegroundColor Green
        Write-Host ("=" * 70)
        Write-Host "Process $ProcessId has stopped."
        Write-Host "Training finished at: $timestamp"
        
        # Show final checkpoint
        if (Test-Path $checkpointPath) {
            Write-Host "`nRunning final checkpoint check..."
            cd g:\Apple_Leaf\ml-training\classification
            python check_checkpoint.py
        }
        
        Write-Host "`n" + ("=" * 70)
        Write-Host "NEXT STEPS:"
        Write-Host "1. Run evaluation:    python evaluate.py"
        Write-Host "2. Run visualization: python visualize.py"
        Write-Host "3. Run Grad-CAM:      python gradcam.py"
        Write-Host ("=" * 70)
        break
    }
    
    # Check checkpoint for progress
    if (Test-Path $checkpointPath) {
        $result = python g:\Apple_Leaf\ml-training\classification\check_checkpoint.py 2>&1 | Out-String
        
        # Extract epoch number
        if ($result -match "Epoch: (\d+)") {
            $currentEpoch = [int]$Matches[1]
            
            if ($currentEpoch -gt $lastEpoch) {
                Write-Host "  Progress: Epoch $currentEpoch completed" -ForegroundColor Cyan
                
                # Extract accuracy
                if ($result -match "Validation Accuracy: ([\d.]+)") {
                    $valAcc = [double]$Matches[1]
                    Write-Host "  Val Accuracy: $($valAcc * 100)%" -ForegroundColor Green
                }
                
                $lastEpoch = $currentEpoch
                $noChangeCount = 0
            } else {
                $noChangeCount++
                Write-Host "  Still on Epoch $currentEpoch (check #$noChangeCount)"
            }
        }
    }
    
    # Show resource usage
    $runtime = ((Get-Date) - $process.StartTime)
    $memory_gb = [math]::Round($process.WS / 1GB, 2)
    Write-Host "  Runtime: $($runtime.Hours)h $($runtime.Minutes)m | Memory: $memory_gb GB"
}

Write-Host "`nMonitoring stopped."
