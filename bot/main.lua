if _G.Executed == nil then
	_G.Executed = true
	local ReplicatedSotrageService = game:GetService("ReplicatedStorage")
	local PlayersService = game:GetService("Players")
	local HttpService = game:GetService("HttpService")


	local WebSocket2 = syn.websocket.connect("ws://localhost:3131")

	local LocalPlayer = PlayersService.LocalPlayer

	local DiscordOrdersChannelID = "1091818089236148255"

	local PlayersOrderDataFileName = "Pending_Orders_Data.txt"

	local TradeRemotesFolder = ReplicatedSotrageService:WaitForChild("Trade", 100)
	local TradeRemotes = {}
	TradeRemotes.SendRequest = TradeRemotesFolder:WaitForChild("SendRequest", 100)
	TradeRemotes.CancelRequest = TradeRemotesFolder:WaitForChild("CancelRequest", 100)
	TradeRemotes.AcceptRequest = TradeRemotesFolder:WaitForChild("AcceptRequest", 100)
	TradeRemotes.DeclineRequest = TradeRemotesFolder:WaitForChild("DeclineRequest", 100)
	TradeRemotes.StartTrade = TradeRemotesFolder:WaitForChild("StartTrade", 100)
	TradeRemotes.OfferItem = TradeRemotesFolder:WaitForChild("OfferItem", 100)
	TradeRemotes.AcceptTrade = TradeRemotesFolder:WaitForChild("AcceptTrade", 100)
	TradeRemotes.DeclineTrade = TradeRemotesFolder:WaitForChild("DeclineTrade", 100)
	--TradeRemotes.DeclineTrade = TradeRemotesFolder:WaitForChild("SendRequest", 100)

	local DefaultChatSystemChatEvents = ReplicatedSotrageService:WaitForChild("DefaultChatSystemChatEvents", 100)
	local SayMessageRequestRemote = DefaultChatSystemChatEvents:WaitForChild("SayMessageRequest", 100)

	--local SynDiscordModule = loadstring(game:HttpGet("https://raw.githubusercontent.com/erotiksamet/syndiscordbackup/main/syndiscordv2.lua"))()
	--local SynDiscordClient = SynDiscordModule.Client.new()

	local PlayersData = {}
	local PlayersOrderData = (isfile(PlayersOrderDataFileName) == true and HttpService:JSONDecode(readfile(PlayersOrderDataFileName))) or {}
	local AllowedAuthorIds = {
		"811149966718271508";
		"773173302549413960";
		"1078380415389290598";
		"545523111915814913";
		"1092470336026595449";
	}

	local VerifiedTable = {}
	for PlayerID, PlayerOrderData in next, PlayersOrderData do
		PlayersOrderData[PlayerID] = nil
		PlayerID = tonumber(PlayerID)
		for _, SubInventoryTab in next, PlayerOrderData.Inventory do
			for ItemName, ItemAmount in next, SubInventoryTab do
				SubInventoryTab[ItemName] = tonumber(ItemAmount)
			end
		end
		PlayerOrderData.PlayerID = PlayerID
		PlayerOrderData.Ready = true
		VerifiedTable[PlayerID] = PlayerOrderData
	end
	PlayersOrderData = VerifiedTable

	function RecordVideoRequest()
		WebSocket2:Send("3131")
	end

	local function UpdatePlayersOrderDataFile()
		writefile(PlayersOrderDataFileName, HttpService:JSONEncode(PlayersOrderData))
	end

	local function BotChatNotification(Message)
		SayMessageRequestRemote:FireServer(Message, "normalchat")
	end

	local function GetPlayerQueuePosition(PlayerClaimTick)
		local TargetPlayerClaimTick, Count = nil, 0
		for _, PlayerData in next, PlayersData do
			TargetPlayerClaimTick = PlayerData.ClaimTick
			if TargetPlayerClaimTick ~= nil and TargetPlayerClaimTick < PlayerClaimTick then
				Count = Count + 1
			end
		end
		return Count
	end

	local function ClaimRequestConnect(PlayerData, Character)
		if PlayerData.Ready == nil then
			PlayerData.Ready = true
			BotChatNotification("Welcome " .. PlayerData.Name .. "! Jump to join the queue and please wait for your turn.")
		end
		PlayerData.Ready = true
		local Humanoid = Character:WaitForChild("Humanoid", 5)
		if Humanoid ~= nil then
			Humanoid:GetPropertyChangedSignal("Jump"):Connect(function()
				if PlayerData.SessionBan == true and tick() - PlayerData.SessionBanStatusTick > 5 then
					PlayerData.SessionBanStatusTick = tick()
					BotChatNotification(PlayerData.Name.." you have reached max warnings... please rejoin and submit new claim request")
				end
				if PlayerData.ClaimTick == nil then
					if PlayersOrderData[PlayerData.UserID] ~= nil then
						PlayerData.ClaimTick = tick()
						BotChatNotification(PlayerData.Name.." your claim request has been registered and current position in queue ["..tostring(GetPlayerQueuePosition(PlayerData.ClaimTick)).."]")
					else
						if tick() - PlayerData.ClaimRejectTick > 5 then
							PlayerData.ClaimRejectTick = tick()
							BotChatNotification(PlayerData.Name.." your claim request has been rejected since you don't have any pending items to claim")
						end
					end
				else
					if tick() - PlayerData.CheckQueuePosTick > 5 then
						PlayerData.CheckQueuePosTick = tick()
						local QueuePosition = GetPlayerQueuePosition(PlayerData.ClaimTick)
						if QueuePosition > 0 then
							BotChatNotification(PlayerData.Name.." your current position in queue ["..tostring(GetPlayerQueuePosition(PlayerData.ClaimTick)).."]")
						end
					end
				end
			end)
		end
	end

	local function RegisterPlayer(Player)
		local PlayerData = {}
		PlayersData[Player] = PlayerData

		PlayerData.ClaimTick = nil
		PlayerData.SessionBan = false
		PlayerData.Warning = 0
		PlayerData.CheckQueuePosTick = 0
		PlayerData.SessionBanStatusTick = 0
		PlayerData.ClaimRejectTick = 0
		PlayerData.Name = Player.Name
		PlayerData.UserID = Player.UserId

		Player.CharacterAdded:Connect(function(Character)
			ClaimRequestConnect(PlayerData, Character)
		end)

		local CurrentCharacter = Player.Character
		if CurrentCharacter ~= nil then
			task.spawn(ClaimRequestConnect, PlayerData, CurrentCharacter)
		end
	end

	local function UnregisterPlayer(Player)
		PlayersData[Player].Left = true
		PlayersData[Player] = nil
	end

	local function IsValidItemDataTab(ItemDataTab)
		if #ItemDataTab > 3 then
			return nil, nil, nil
		end
		local ItemName, ItemAmount, ItemType = unpack(ItemDataTab)
		if ItemType ~= "Pets" and ItemType ~= "Weapons" then
			return nil, nil, nil
		end
		ItemAmount = tonumber(ItemAmount)
		if ItemAmount == nil or ItemAmount <= 0 then
			return nil, nil, nil
		end
		return ItemName, ItemAmount, ItemType
	end

	local function IsInventoryEmpty(PlayerOrderInventory)
		for _,_ in next, PlayerOrderInventory.Pets do
			return false
		end
		for _,_ in next, PlayerOrderInventory.Weapons do
			return false
		end
		return true
	end

	local function OnDiscordMessage(Message)
		if type(Message) == "string" then
			print(Message)
			local ContentLines = Message.content:split("\n")

			local PlayerID = tonumber(ContentLines[1])
			table.remove(ContentLines, 1)

			if PlayerID ~= nil then
				local PlayerOrderData = PlayersOrderData[PlayerID]
				if PlayerOrderData == nil then
					PlayerOrderData = {}
					PlayersOrderData[PlayerID] = PlayerOrderData
					PlayerOrderData.PlayerID = PlayerID
					PlayerOrderData.Inventory = {["Pets"] = {}; ["Weapons"] = {}}
				end

				local PlayerOrderInventory, SubInventoryTab, ItemDataTab = PlayerOrderData.Inventory, nil, nil
				for _, ItemDataString in next, ContentLines do
					local ItemName, ItemAmount, ItemType = IsValidItemDataTab(string.split(ItemDataString, ":"))
					if ItemName ~= nil then
						SubInventoryTab = PlayerOrderInventory[ItemType]
						--warn(PlayerID, ItemType, ItemName)
						if SubInventoryTab[ItemName] ~= nil then
							SubInventoryTab[ItemName] = SubInventoryTab[ItemName] + ItemAmount
						else
							SubInventoryTab[ItemName] = ItemAmount
						end
					end
				end

				if IsInventoryEmpty(PlayerOrderInventory) == true then
					PlayersOrderData[PlayerID] = nil
				else
					task.spawn(UpdatePlayersOrderDataFile)
					PlayerOrderData.Ready = true
					--Message.react('👍')
				end
			end
		end
	end

	local DeclineRequestTick = 0
	local CompletedTradeTick = 0
	local DeclineTradeTick = 0
	local SendRequestTick = 0
	local StartTradeTick = 0

	local TradeBusyBool = false
	local ListedItemsBool = false
	local PerformingTradeBool = false

	local ListedWeapons, ListedPets = {}, {}

	local function OnDeclineRequest()
		DeclineRequestTick = tick()
	end

	local function OnDeclineTrade()
		DeclineTradeTick = tick()
	end

	local function OnAcceptTrade(CompletedTrade)
		if CompletedTrade == true then
			CompletedTradeTick = tick()
		else
			if ListedItemsBool == true then
				TradeRemotes.AcceptTrade:FireServer()
			end
		end
	end

	local function OnPerformingTradeChanged()
		if LocalPlayer:GetAttribute("PerformingTrade") == true then
			PerformingTradeBool = true
		end
	end

	local function OnStartTrade(_, PlayerName)
		TradeBusyBool, ListedItemsBool, PerformingTradeBool, StartTradeTick = true, false, false, tick()
		local PlayerData = PlayersData[PlayersService:FindFirstChild(PlayerName)]
		if PlayerData ~= nil and PlayerData.Ready == true then
			local PlayerOrderData = PlayersOrderData[PlayerData.UserID]
			if PlayerOrderData ~= nil and PlayerOrderData.Ready == true then
				table.clear(ListedWeapons)
				table.clear(ListedPets)

				task.spawn(RecordVideoRequest)

				local MaxItemTypeCount = 0
				local OrderWeaponsInventory, OrderPetsInventory = PlayerOrderData.Inventory.Weapons, PlayerOrderData.Inventory.Pets
				for ItemName, ItemAmount in next, OrderWeaponsInventory do
					if MaxItemTypeCount < 4 then
						for ItemCount = 1, ItemAmount do
							TradeRemotes.OfferItem:FireServer(ItemName, "Weapons")
						end
						ListedWeapons[ItemName] = ItemAmount
						MaxItemTypeCount = MaxItemTypeCount + 1
					else
						break
					end
				end
				for ItemName, ItemAmount in next, OrderPetsInventory do
					if MaxItemTypeCount < 4 then
						for ItemCount = 1, ItemAmount do
							TradeRemotes.OfferItem:FireServer(ItemName, "Pets")
						end
						ListedPets[ItemName] = ItemAmount
						MaxItemTypeCount = MaxItemTypeCount + 1
					else
						break
					end
				end
				ListedItemsBool = true
				BotChatNotification(PlayerName.." i have added the items so please accept the trade in 10 seconds otherwise it will be cancelled")
				--TradeRemotes.AcceptTrade:FireServer()

				local SafetyBool, ClientDeclinedTrade = false, nil
				while task.wait(0) do
					if ((DeclineTradeTick > StartTradeTick) or (tick() - StartTradeTick > 12)) and PerformingTradeBool == false then
						--warn(DeclineTradeTick > StartTradeTick, tick() - StartTradeTick, tick() - StartTradeTick >= 10)
						if SafetyBool == false then
							ClientDeclinedTrade = (DeclineTradeTick > StartTradeTick)
							TradeRemotes.DeclineTrade:FireServer()
							SafetyBool = true
							task.wait((ClientDeclinedTrade == true and 1) or 3)
						else
							TradeRemotes.DeclineTrade:FireServer()
							--PlayerData.BanTick = tick()
							--PlayerData.ClaimTick = tick()
							if PlayerData.Warning >= 2 then
								PlayerData.SessionBan = true
								BotChatNotification(PlayerName.." you have reached max warnings... please rejoin and submit new claim request")
							else
								PlayerData.Warning = PlayerData.Warning + 1
								if ClientDeclinedTrade == true then
									BotChatNotification(PlayerName.." you have been warned for rejecting the trade [Total Warnings "..tostring(PlayerData.Warning).."/3]")
								else
									BotChatNotification(PlayerName.." you have been warned for not accepting the trade in 10 seconds [Total Warnings "..tostring(PlayerData.Warning).."/3]")
								end
							end
							break
						end
					end
					if (CompletedTradeTick > StartTradeTick) then
						--warn(CompletedTradeTick > StartTradeTick)
						for ItemName, ItemAmount in next, ListedWeapons do
							--warn(ItemName)
							if OrderWeaponsInventory[ItemName] == ItemAmount then
								OrderWeaponsInventory[ItemName] = nil
							else
								OrderWeaponsInventory[ItemName] = OrderWeaponsInventory[ItemName] - ItemAmount
							end
						end
						for ItemName, ItemAmount in next, ListedPets do
							--warn(ItemName)
							if OrderPetsInventory[ItemName] == ItemAmount then
								OrderPetsInventory[ItemName] = nil
							else
								OrderPetsInventory[ItemName] = OrderPetsInventory[ItemName] - ItemAmount
							end
						end
						if IsInventoryEmpty(PlayerOrderData.Inventory) == true then
							--warn("EMPTY")
							PlayersOrderData[PlayerData.UserID] = nil
							PlayerData.ClaimTick = nil
							BotChatNotification(PlayerName.." Trade Completed Succesfully!!! you have claimed all your items")
						else
							BotChatNotification(PlayerName.." Trade Completed Succesfully!!! you still have items left to claim")
						end

						task.spawn(UpdatePlayersOrderDataFile)

						break
					end
				end
			else
				TradeRemotes.DeclineTrade:FireServer()
			end
		else
			TradeRemotes.DeclineTrade:FireServer()
		end
		TradeBusyBool = false
	end

	local function GetPlayerWithOrder()
		local CurrentPlayer, CurrentPlayerData, CurrentPlayerOrderData, CurrentPlayerClaimTick = nil, nil, nil, nil

		local PlayerOrderData
		for Player, PlayerData in next, PlayersData do
			if PlayerData.Ready == true and PlayerData.SessionBan == false and PlayerData.ClaimTick ~= nil then
				PlayerOrderData = PlayersOrderData[PlayerData.UserID]
				if PlayerOrderData ~= nil and PlayerOrderData.Ready == true and (CurrentPlayerClaimTick == nil or PlayerData.ClaimTick >= CurrentPlayerClaimTick) then
					CurrentPlayer, CurrentPlayerData, CurrentPlayerOrderData, CurrentPlayerClaimTick = Player, PlayerData, PlayerOrderData, PlayerData.ClaimTick
				end
			end
		end

		return CurrentPlayer, CurrentPlayerData, CurrentPlayerOrderData
	end

	LocalPlayer:GetAttributeChangedSignal("PerformingTrade"):Connect(OnPerformingTradeChanged)

	TradeRemotes.DeclineRequest.OnClientEvent:Connect(OnDeclineRequest)
	TradeRemotes.DeclineTrade.OnClientEvent:Connect(OnDeclineTrade)
	TradeRemotes.AcceptTrade.OnClientEvent:Connect(OnAcceptTrade)
	TradeRemotes.StartTrade.OnClientEvent:Connect(OnStartTrade)
	TradeRemotes.SendRequest.OnClientInvoke = function()
		return false
	end

	--SynDiscordClient:on("ready", function() warn("Murder Mystery 2 Trading Bot Ready!!!") end)
	--SynDiscordClient:on("messageCreate", OnDiscordMessage)
	--SynDiscordClient:login("OTM5MjMyOTk1ODI1NTc0MDMz.GfNHBv.gqks649uHRsmkVuvMpLj_9DbsKy64Dmh26yVQk")
	
	WebSocket2.OnMessage:Connect(OnDiscordMessage)

	PlayersService.PlayerAdded:Connect(RegisterPlayer)
	PlayersService.PlayerRemoving:Connect(UnregisterPlayer)
	for _, Player in next, PlayersService:GetPlayers() do
		if Player ~= LocalPlayer then
			task.spawn(RegisterPlayer, Player)
		end
	end

	while task.wait(0) do
		if TradeBusyBool == false then
			local Player, PlayerData, PlayerOrderData = GetPlayerWithOrder()
			if Player ~= nil then
				SendRequestTick = tick()
				if not TradeRemotes.SendRequest:InvokeServer(Player) then
					BotChatNotification(PlayerData.Name.." i have sent you a trade request please accept it in 7 seconds")
					while task.wait(0) and TradeBusyBool == false do
						if (DeclineRequestTick > SendRequestTick) or (tick() - SendRequestTick > 7) then
							TradeRemotes.CancelRequest:FireServer()
							PlayerData.ClaimTick = tick()
							if DeclineRequestTick > SendRequestTick then
								BotChatNotification(PlayerData.Name.." you declined the trade request..."..((GetPlayerQueuePosition(PlayerData.ClaimTick) > 0 and " so i have reset your queue position to "..tostring(GetPlayerQueuePosition(PlayerData.ClaimTick))) or " please accept the next trade request!"))
							else
								BotChatNotification(PlayerData.Name.." you failed to accept trade request in 7 seconds..."..((GetPlayerQueuePosition(PlayerData.ClaimTick) > 0 and " so i have reset your queue position to "..tostring(GetPlayerQueuePosition(PlayerData.ClaimTick))) or " please accept the next trade request!"))
							end
							task.wait(1)
							break
						end
					end
				else
					PlayerData.ClaimTick = nil
					BotChatNotification(PlayerData.Name.." failed to send you trade request because your trading is disabled"..((GetPlayerQueuePosition(PlayerData.ClaimTick) > 0 and " and recheck your new queue position") or ""))
				end
			end
		end
	end
end