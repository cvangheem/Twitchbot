from twitchbot import (
    Message,
    add_custom_command,
    get_custom_command,
    delete_custom_command,
    custom_command_exist,
    CustomCommand,
    session,
    cfg,
    Command,
    InvalidArgumentsError, same_channel_predicate)

PERMISSION = 'manage_commands'

PREFIX = cfg.prefix
BLACKLISTED_PREFIX_CHARACTERS = './'

import pyttsx3
import time
import random
import collections
import math
from beepy import beep
import flask_app as fa

# sound argument takes either integers (1-7) or string (from the list below) as argument.
# Following are the mappings for the numbers: 1 : 'coin', 2 : 'robot_error', 3 : 'error', 4 : 'ping', 5 : 'ready', 6 : 'success', 7 : 'wilhelm'

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)

def _verify_resp_is_valid(resp: str):
    return resp[0] not in BLACKLISTED_PREFIX_CHARACTERS


@Command('addcmd', permission=PERMISSION, syntax='<name> <response>',
         help='adds a custom command to the database for the this channel, '
              'placeholders: %user : the name of the person that triggered the command,'
              '%uptime : the channels live uptime,'
              '%channel : the channels name')
async def cmd_add_custom_command(msg: Message, *args):
    if len(args) < 2:
        raise InvalidArgumentsError(reason='missing required arguments', cmd=cmd_add_custom_command)

    name, resp = args[0], ' '.join(args[1:])
    name = name.lower()

    if not _verify_resp_is_valid(resp):
        raise InvalidArgumentsError(reason='response cannot have . or / as the starting character',
                                    cmd=cmd_add_custom_command)

    if custom_command_exist(msg.channel_name, name):
        raise InvalidArgumentsError(reason='custom command already exist by that name',
                                    cmd=cmd_add_custom_command)

    if add_custom_command(CustomCommand.create(msg.channel_name, name, resp)):
        await msg.reply('successfully added command')
    else:
        await msg.reply('failed to add command')


@Command('updatecmd', permission=PERMISSION, syntax='<name> <response>',
         help="updates a custom command's response message")
async def cmd_update_custom_command(msg: Message, *args):
    if len(args) < 2:
        raise InvalidArgumentsError(reason='missing required arguments', cmd=cmd_update_custom_command)

    name, resp = args[0], ' '.join(args[1:])
    name = name.lower()

    if not _verify_resp_is_valid(resp):
        raise InvalidArgumentsError(reason='response cannot have . or / as the starting character',
                                    cmd=cmd_update_custom_command)

    cmd = get_custom_command(msg.channel_name, name)
    if cmd is None:
        raise InvalidArgumentsError(reason=f'custom command "{name}" does not exist', cmd=cmd_update_custom_command)

    cmd.response = resp
    session.commit()

    await msg.reply(f'successfully updated {cmd.name}')


@Command('delcmd', permission=PERMISSION, syntax='<name>', help='deletes a custom commands')
async def cmd_del_custom_command(msg: Message, *args):
    if not args:
        raise InvalidArgumentsError(reason='missing required arguments', cmd=cmd_del_custom_command)

    cmd = get_custom_command(msg.channel_name, args[0].lower())
    if cmd is None:
        raise InvalidArgumentsError(reason=f'no command found for "{args[0]}"', cmd=cmd_del_custom_command)

    if delete_custom_command(msg.channel_name, cmd.name):
        await msg.reply(f'successfully deleted command {cmd.name}')
    else:
        await msg.reply(f'failed to delete command {cmd.name}')


@Command('cmd', syntax='<name>', help='gets a custom commmands response')
async def cmd_get_custom_command(msg: Message, *args):
    if not args:
        raise InvalidArgumentsError(reason='missing required arguments', cmd=cmd_get_custom_command)

    cmd = get_custom_command(msg.channel_name, args[0].lower())
    if cmd is None:
        raise InvalidArgumentsError(reason=f'no command found for "{args[0]}"', cmd=cmd_get_custom_command)

    await msg.reply(f'the response for "{cmd.name}" is "{cmd.response}"')


@Command('testreply')
async def cmd_test_reply(msg: Message, *args):
    await msg.reply('hello! enter your name:')
    reply = await msg.wait_for_reply(default='you didnt reply, how sad :(', timeout=30)
    await msg.reply(f'you entered: {reply.content}')


@Command('s', permission=PERMISSION, syntax='<word>', help='gets Bot to speak')
async def cmd_speak(msg: Message, *args):
    speech_text = ' '.join(args)
    await msg.reply(speech_text)
    beep(sound=1)
    engine.say(speech_text)
    engine.runAndWait()
    fa.print_answer(speech_text)

@Command('a_speech', permission=PERMISSION)
async def cmd_anarchy_speech(msg: Message, *args):
    await msg.reply('What does Bott say? Submit your answer in the chat.')
    anarchy_dialogue = []
    t_end = time.time() + 10
    while time.time() < t_end:
        reply = await msg.wait_for_reply(predicate=same_channel_predicate(msg), timeout=10)
        anarchy_dialogue.append(reply.content)
    else:
        answer = random.choice(anarchy_dialogue)
        if answer == "None":
            await msg.reply("Bott has nothing to say.")
            beep(sound=2)
        else:
            beep(sound=1)
            await msg.reply(answer)
            engine.say(answer)
            engine.runAndWait()


@Command('d_speech', permission=PERMISSION)
async def cmd_democracy_speech(msg: Message, *args):
    await msg.reply('What does Bott say? Submit your answer in the chat.')
    democracy_dialogue = []
    t_end = time.time() + 10
    while time.time() < t_end:
        reply = await msg.wait_for_reply(predicate=same_channel_predicate(msg), timeout=10)
        if reply.content == "None":
            pass
        elif reply.content == '':
            pass
        else:
            democracy_dialogue.append(reply.content)
    else:
        if len(democracy_dialogue) == 1:
            await msg.reply(democracy_dialogue[0])
            beep(sound=1)
            engine.say(str(democracy_dialogue[0]))
            engine.runAndWait()
        elif len(democracy_dialogue) == 2:
            new_list = random.sample(democracy_dialogue, 2)
            await msg.reply("Vote on what Bott says: \n" + "1: " + new_list[0] + "\n" + "2: " + new_list[
                1] + ". Submit your vote in the chat.")
        elif len(democracy_dialogue) == 3:
            new_list = random.sample(democracy_dialogue, 3)
            await msg.reply(
                "Vote on what Bott says: \n" + "1: " + new_list[0] + "\n" + "2: " + new_list[1] + "\n" + "3: " +
                new_list[2] + ". Submit your vote in the chat.")
        elif len(democracy_dialogue) == 4:
            new_list = random.sample(democracy_dialogue, 4)
            await msg.reply(
                "Vote on what Bott says: \n" + "1: " + new_list[0] + "\n" + "2: " + new_list[1] + "\n" + "3: " +
                new_list[2] + "\n" + "4: " + new_list[3] + "\n" + ". Submit your vote in the chat.")
        else:
            new_list = random.sample(democracy_dialogue, 5)
            await msg.reply(
                "Vote on what Bott says: \n" + "1: " + new_list[0] + "\n" + "2: " + new_list[1] + "\n" + "3: " +
                new_list[2] + "\n" + "4: " + new_list[3] + "\n" + "5: " + new_list[
                    4] + ". Submit your vote in the chat.")
    votes = []
    v_end = time.time() + 10
    while time.time() < v_end:
        vote_reply = await msg.wait_for_reply(predicate=same_channel_predicate(msg), timeout=10)
        votes.append(vote_reply.content)
    else:
        vote_count = collections.Counter(votes)
        max_votes = max(vote_count.values())
        lst = [i for i in vote_count.keys() if vote_count[i] == max_votes]
        vote_answer = sorted(lst)[0]
        if vote_answer == "None":
            await msg.reply("Bott has nothing to say.")
            beep(sound=2)
        elif vote_answer == "1":
            await msg.reply(new_list[0])
            beep(sound=1)
            engine.say(str(new_list[0]))
            engine.runAndWait()
        elif vote_answer == "2":
            await msg.reply(new_list[1])
            beep(sound=1)
            engine.say(str(new_list[1]))
            engine.runAndWait()
        elif vote_answer == "3":
            await msg.reply(new_list[2])
            beep(sound=1)
            engine.say(str(new_list[2]))
            engine.runAndWait()
        elif vote_answer == "4":
            await msg.reply(new_list[3])
            beep(sound=1)
            engine.say(str(new_list[3]))
            engine.runAndWait()
        elif vote_answer == "5":
            await msg.reply(new_list[4])
            beep(sound=1)
            engine.say(str(new_list[4]))
            engine.runAndWait()
        else:
            await msg.reply("Bott has nothing to say.")
            beep(sound=2)


@Command('movement', syntax='pos1', permission=PERMISSION)
async def cmd_movement(msg: Message, *args):
    await msg.reply('Submit a space for Bott to move to in the chat: ')
    movement_choices = []
    t_end = time.time() + 10
    while time.time() < t_end:
        move_reply = await msg.wait_for_reply(predicate=same_channel_predicate(msg), timeout=10)
        start_move = ' '.join(args)
        pos1 = start_move.upper()
        raw_move_reply = move_reply.content
        pos2 = raw_move_reply.upper()
        if len(str(pos2)) != 2:
            pass
        if len(str(pos2)) == 2:
            pos1_ascii = [ord(c) for c in pos1]
            pos2_ascii = [ord(c) for c in pos2]
            delta = [pos2_ascii[0] - pos1_ascii[0], pos2_ascii[1] - pos1_ascii[1]]
            distance = math.sqrt(delta[0] ** 2 + delta[1] ** 2)
            rnd_d = math.ceil(distance)
            if rnd_d > 6:
                await msg.reply('Bott cannot move to space ' + pos2)
            else:
                movement_choices.append(pos2)
    else:
        movement_count = collections.Counter(movement_choices)
        dict = {}
        for value in movement_count.values():
            dict[value] = []
        for (key, value) in movement_count.items():
            dict[value].append(key)
        if len(dict) == 1:
            top_movement = sorted(dict.keys(), reverse=True)[0]
            await msg.reply(dict[top_movement][0])
            beep(sound=1)
            engine.say(str(dict[top_movement][0]))
            engine.runAndWait()
        elif len(dict) == 2:
            top_movement = sorted(dict.keys(), reverse=True)[0]
            second_movement = sorted(dict.keys(), reverse=True)[1]
            await msg.reply(dict[top_movement][0] + ', ' + dict[second_movement][0])
            beep(sound=1)
            engine.say(str(dict[top_movement][0]))
            engine.runAndWait()
        elif len(dict) >= 3:
            top_movement = sorted(dict.keys(), reverse=True)[0]
            second_movement = sorted(dict.keys(), reverse=True)[1]
            third_movement = sorted(dict.keys(), reverse=True)[2]
            await msg.reply(dict[top_movement][0] + ', ' + dict[second_movement][0] + ', ' + dict[third_movement][0])
            beep(sound=1)
            engine.say(str(dict[top_movement][0]))
            engine.runAndWait()
        else:
            await msg.reply("Bott doesn't know where to go.")
            beep(sound=2)
