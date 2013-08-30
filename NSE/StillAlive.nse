description=[[
Nothing to Say here
]]

categories = {"safe", "discovery"}

require("nmap")
require("os")
require("stdnse")
require("http")
require("io")
require("socket.url")

function setupLogs()
	logFile = io.open("script.log", "a")
end

function closeLogs()
	if logFile ~= nil then
		logFile:close()
	end
end

function writeLog(ip, timestamp, state, response)
	if logFile ~= nil then
		logFile:write(ip.."\t");
		logFile:write(timestamp.."\t")		
		logFile:write(state.."\t")
			
		local str = ""

		if type(response) == "string" then
			str = response
		elseif type(response) == "table" then
			str = tableToString(response)
		end
		
		str = url.escape(str)
		str = replacePercentage(str)
		logFile:write(str)

		logFile:write("\r\n")
	end
end

function replacePercentage(str)
	return str:gsub("%%", "=")
end

function tableToString(table)
	local output = ""
	
	if table ~= nil then
		if type(table) == "table" then
			for k,v in pairs(table) do
				if k == "status-line" or k =="rawheader" or k == "body" then
					if v ~= nil  then
						if type(v) == "table" then
							output = output..tableToString(v)	
						else
							output = output..v
						end
					end
				end
			end	
		end
	end

	return output
end

function portrule(host, port)
	return true
end

function prerule(host, port)
	return true
end

action = function(host, port)

	local getrequest = http.get(host, port, "/")	
	writeLog(host.ip, os.time(), port.state, getrequest)
	
	closeLogs()
	
	return "Finished"
end

setupLogs()
