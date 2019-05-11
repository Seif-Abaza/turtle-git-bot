"""

making_issue = original_message = repo_name = issue_title = issue_body = False

reserved_commands = ['makeissue', 'cancel']


class MyClient(discord.Client):

	channel = None

	try:

		async def sent_reserved_command(self, info, new_issue=False):
			global channel
			try:
				reserved_no = reserved_commands.index(info)
				existing_thing = reserved_commands[reserved_no]
				if existing_thing == 'makeissue':
					if not new_issue:
						await channel.send("Already making issue, use '!git cancel' to cancel current process")
						return "restart"
					else:
						return
				elif existing_thing == 'cancel':
					await channel.send("Cancelling operation...")
					return "exit"
				else:
					return
			except:
				traceback.print_exc()
				return

		async def make_issue(self, info=None, new_issue= False):
			global making_issue, repo_name, issue_title, issue_body
			making_issue = True

			def check(m):
				global original_message
				return m.channel == original_message.channel and m.author == original_message.author

			sent_reserved = await self.sent_reserved_command(info=original_message.content[5:], new_issue=new_issue)
			if sent_reserved == 'exit':
				print("exiting")
				return
			elif sent_reserved == "restart":
				return
			else:
				pass

			if not repo_name:
				if not info:
					await channel.send("It seems you'd like to make an issue! Let's continue. Type `!git cancel` at any time to cancel the process.")
					await channel.send("**Please enter the name of the repository to which you'd like to submit an issue!** \n*Eg: `!git turtlecoin-wallet-electron`*")
					while not repo_name:
						try:
							repo_name = await client.wait_for('message', check=check, timeout=30.0)
							repo_name = repo_name.content[5:]
						except:
							traceback.print_exc()
						
			if not issue_title:
				if not info:
					await channel.send("**Please enter the title of the issue** \n*Eg: `!git Issue with sending transaction`*")
					try:
						issue_title = await client.wait_for('message', check=check, timeout=30.0)
						issue_title = issue_title.content[5:]
					except:
						traceback.print_exc()

			if not issue_body:
				if not info:
					await channel.send("\n**Please enter any extra info in the body of the issue! Optional, but recommended!**\n*Eg: `!git Descriptive information on the issue`* \n*Type `!git` to skip this step*\n")
					try:
						issue_body = await client.wait_for('message', check=check, timeout=30.0)
						if issue_body.content[3:] != '':
							issue_body = issue_body.content[5:]
						else: # it's empty, wants to skip
							pass
					except:
						traceback.print_exc()

			if repo_name and issue_title:

				await channel.send('Making issue...')
			
				try:
					repo = g.get_repo(f'Soja8/{repo_name}')
					made_issue = repo.create_issue(title=issue_title, body=issue_body)
					issue_number = made_issue.number
					made_issue_link = f"https://github.com/soja8/{repo_name}/issues/{issue_number}" # NOTE: CHANGE THIS
					await channel.send(f'All done! The issue was succesfully made! \nLink: {made_issue_link}')
				except Exception as e:
					await channel.send("Some error occured, please try again!")
					await channel.send(e)

			repo_name=issue_title=issue_body=making_issue=False
			return

		async def on_message(self, message):
			global original_message, channel, making_issue

			# get channel info to send info to
			channel = client.get_channel(536397649671356418)
			# NOTE: might remove this line, make it respond in the same channel it was called. or check if it's not in any but dev_ channels

			# if the bot sent the message ignore it
			if message.author == client.user:
				return

			original_message = message

			inputed = message.content.split(" ")

			if inputed[0] != "!git":
				return
			
			thing_to_do = inputed[1:]

			if not making_issue:
				try:
					if thing_to_do[0] == 'makeissue':
						await self.make_issue(new_issue=True)
					else:
						return
				except:
					traceback.print_exc()
					return
			else: # currently in the process of making an issue
				await self.make_issue(info=thing_to_do)
		
		async def on_ready(self):

			# let us know we're ready
			print('Logged on as {0}!'.format(self.user))

			channel = client.get_channel(536397649671356418)

			# send for da ez confirmation
			await channel.send('GitHub bot is up!')

	except Exception as e:
		traceback.print_exc()
		
		
# connect to discord
client = MyClient()
client.run(token)
"""

#bot = 