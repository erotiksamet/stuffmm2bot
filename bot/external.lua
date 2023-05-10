local args = {
    [1] = {
        ["1v1Mode"] = false,
        ["Disguises"] = false,
        ["1v1ModeAuto"] = false,
        ["LobbyMode"] = true,
        ["DeadCanTalk"] = false,
        ["LockFirstPerson"] = false,
        ["Assassin"] = false
    }
}
warn("Custom Game Settings Updated")
game:GetService("ReplicatedStorage").Remotes.CustomGames.UpdateServerSettings:FireServer(unpack(args))

local Players = game:GetService("Players")
local GC = getconnections or get_signal_cons

if GC then
    for _, connection in ipairs(GC(Players.LocalPlayer.Idled)) do
        if connection["Disable"] then
            connection["Disable"](connection)
        elseif connection["Disconnect"] then
            connection["Disconnect"](connection)
        end
    end
end
warn("Anti AFK Enabled")