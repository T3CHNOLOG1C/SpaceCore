from discord.ext.commands import check


def is_owner():
    return check((lambda ctx: ctx.bot.owner_role in ctx.message.author.roles))


def is_admin():
    return check((lambda ctx: ctx.bot.admin_role in ctx.message.author.roles))

def is_mod():
    return check((lambda ctx: ctx.bot.admin_role in ctx.message.author.roles))


def is_staff():
    return is_owner() or is_admin() or is_mod()
