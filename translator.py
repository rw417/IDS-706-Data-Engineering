import click
import deep_translator
import pandas as pd

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def main():
    """
    A simple CLI tool for translation.
    """
    return


@click.command(hidden=True)
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())


@click.command()
@click.option(
    "--text",
    prompt="Text to translate",
    default="",
    show_default=False,
    help="Enter the text you would like to translate here",
)
@click.option(
    "--source",
    prompt="Source language",
    default="auto",
    show_default=True,
    help="Specify the language of the text you entered. Leave blank to use auto detection",
)
@click.option(
    "--target",
    prompt="Target language",
    help="Specify the lanauge to translate to. You cannot leave it blank.",
)
def translate(text, source, target):
    """
    Translates the your text to the target language you specify.

    Your text should not exceed 5,000 words.

    The source and target should be two-letter codes. To see the code for each language, use the command 'code'.
    """
    # if no text entered, return blank
    if len(text) == 0:
        click.echo("")
    # if source and target are the same, return this message
    elif source == target:
        click.echo(
            f"""
#######
Result
#######

Specified source language: {source}
Specified target language: {target}

Your source and target languages are the same! Below is the text you wanted to translate:
{text}"""
        )

    elif source == "auto":
        # detect the language of source
        s = deep_translator.single_detection(
            text, api_key="a6ad632bb89546dd29679a8657b1b471"
        )
        # if they're the same, return this message
        if s == target:
            click.echo(
                f"""
#######
Result
#######

Detected source language: {s}
Specified target language: {target}

Your source and target languages are the same! Below is the text you wanted to translate:
{text}"""
            )
        # if they're not the same, get translation
        else:
            source = s
            translated = deep_translator.GoogleTranslator(s, target).translate(text)
            click.echo(
                f"""
#######
Result
#######

Detected source language: {s}
Specified target language: {target}
Input text: {text}
Translation: {translated}"""
            )

    # if source was specified
    else:
        translated = deep_translator.GoogleTranslator(source, target).translate(text)
        click.echo(
            f"""
#######
Result
#######

Specified source language: {source}
Specified target language: {target}
Input text: {text}
Translation: {translated}"""
        )
        
        # check if detected source language agrees with what the user specified
        s = deep_translator.single_detection(
            text, api_key="a6ad632bb89546dd29679a8657b1b471"
        )
        if s != source:
            click.echo(f"""\nCAUTION:\nYou specified the source language to be '{source}', but the text looks like '{s}'. Please double check.""")
        


@click.command()
@click.option(
    "--language",
    prompt="Name of language. Leave blank to see all codes",
    default="",
    help="Enter the English name of the language to see the two-letter code. Leave blank to see all codes.",
)
def code(language):
    """
    Produces the two-letter code of a language for you to input as the source or target language in "translate"
    """
    langs_dict = deep_translator.GoogleTranslator.get_supported_languages(as_dict=True)
    if language == "":
        langs_df = pd.DataFrame.from_dict(langs_dict, columns=[0], orient="index")
        langs_df.reset_index(level=0, inplace=True)
        langs_df = langs_df.rename(columns={"index": "language", 0: "code"})
        click.echo(langs_df.to_string())
    else:
        try:
            language_lower = language.lower()
            lang_code = langs_dict[language_lower]
            click.echo(f'The code for "{language}"" is {lang_code}')
        except KeyError as ke:
            click.echo(f'Sorry, but "{language}" is not a supported language')


main.add_command(help)
main.add_command(translate)
main.add_command(code)

if __name__ == "__main__":
    main()
