def idsFromPings(message):
	ids = re.findall(r"<@[\!\&]([0-9]+)>", message)
	if len(ids) == 0:
		return None
	elif len(ids) == 1:
		return ids[0]
	else:
		return ids
