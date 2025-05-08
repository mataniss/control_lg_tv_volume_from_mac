local function sendCurlIfLGTV()
    local output = hs.audiodevice.defaultOutputDevice():name()
    if output == "LG TV" then
        hs.timer.doAfter(1, function()
            hs.execute("curl -X GET http://localhost:5001/api/refreshKeysListener", true)
            hs.alert("Triggered refresh (LG TV)")
        end)
    else
        hs.alert("Skipped refresh (Output: " .. output .. ")")
    end
end

-- Watch for unlock events
local unlockWatcher = hs.caffeinate.watcher.new(function(event)
    if event == hs.caffeinate.watcher.screensDidUnlock then
        sendCurlIfLGTV()
    end
end)
unlockWatcher:start()

-- Watch for screen resolution or display changes
local screenWatcher = hs.screen.watcher.new(function()
    sendCurlIfLGTV()
end)
screenWatcher:start()
