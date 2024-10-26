from bot.modules.database.mongodb import MongoDB
from bot.helper.telegram_helper import Message, Button
from datetime import datetime, timedelta
from bot.modules.quizzes.quizz_parameters import QuizParameters
class SubsManager:
    """Class to manage the user's coin usage and premium status."""

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_data = None
        self.preimum_quiz_coins = 1
        self.gpt_coins = 2
        self.imagine_coins = 5
        self.summary_coins = 10

    async def _get_user_data(self):
        """Fetch user data from the database."""
        self.user_data = await MongoDB.find_one("users", "user_id", self.user_id)
        return self.user_data

    async def _update_user_field(self, field, value):
        """Update a specific field in the user's database entry."""
        await MongoDB.update_db("users", "user_id", self.user_id, field, value)

    async def _update_user_coins(self, new_coin_balance):
        """Update the user's remaining coins."""
        await self._update_user_field("reminig_premium_quizzes", new_coin_balance)

    async def get_remaining_coins(self):
        """Get the user's remaining coins (quizzes)."""
        user_data = await self._get_user_data()
        return user_data.get("reminig_premium_quizzes", 0)

    async def set_remaining_coins(self, new_coin_balance):
        """Set the user's remaining coins to a new value."""
        await self._update_user_coins(new_coin_balance)

    async def use_coins(self, amount):
        """Deduct a specific number of coins from the user's balance."""
        remaining_coins = await self.get_remaining_coins()
        if remaining_coins < amount:
            raise ValueError("Not enough coins.")
        await self._update_user_coins(remaining_coins - amount)

    # Specific usage handlers
    async def use_quiz(self):
        """Deduct 1 coin for a quiz."""
        await self.use_coins(self.preimum_quiz_coins)

    async def use_summarization(self):
        """Deduct 10 coins for a summarization."""
        await self.use_coins(self.summary_coins)

    async def use_image_generation(self):
        """Deduct 5 coins for image generation."""
        await self.use_coins(self.imagine_coins)

    async def use_question_ask(self):
        """Deduct 2 coins for asking a question."""
        await self.use_coins(self.gpt_coins)

    # New methods to handle premium status and expiration

    async def check_premium_status(self):
        """Check if the user's premium subscription is still valid."""
        user_data = await self._get_user_data()
        premium_expiration = user_data.get("premium_expiration")

        if premium_expiration:
            expiration_date = datetime.fromisoformat(premium_expiration)
            if expiration_date < datetime.utcnow():
                # Subscription expired, set coins to 0 and remove premium status
                await self.set_remaining_coins(0)
                await self._update_user_field("premium", False)
                return False  # User is no longer premium
        return user_data.get("premium", False)

    async def get_remaining_premium_days(self):
        """Get the number of days remaining in the user's premium subscription."""
        user_data = await self._get_user_data()
        premium_expiration = user_data.get("premium_expiration")

        if premium_expiration:
            expiration_date = datetime.fromisoformat(premium_expiration)
            remaining_time = expiration_date - datetime.utcnow()
            return max(remaining_time.days, 0)
        return 0

    # Example of adding coins (could be useful for premium upgrades, bonuses, etc.)
    async def _add_coins(self, amount):
        """Add a specific number of coins to the user's balance."""
        remaining_coins = await self.get_remaining_coins()
        await self._update_user_coins(remaining_coins + amount)

    async def _add_subs_user_id(self):
        await self._update_user_field("premium", True)

    async def _add_monthes(self, monthes):
        current_date = datetime.utcnow()
        premium_expiration = current_date + timedelta(days=monthes * 30)
        await self._update_user_field("premium_expiration", premium_expiration.isoformat())

    async def subscriber_user(self, is_premium=True, subscription_month=1, subscription_quizzes=2000):
        await self._add_subs_user_id()
        await self._add_monthes(subscription_month)
        await self._add_coins(subscription_quizzes)

        await Message.send_msg(self.user_id, f"<b>Congratulations!</b> 🥳 \nYou have been subscribed to premium for {subscription_month} months. You have been given {subscription_quizzes} Coins🪙. \nEnjoy your premium subscription⚡!\nWith love from @osama_mo7💓" )
        
    async def validate_user_subscription(self, update, program, context):
        """
        Validates user subscription and premium status using SubsManager.
        :parma update: The Telegram update object.
        :param program: The program for which the subscription is being validated can be ["p_quiz", "summary", "imagine", "gpt"].
        """
        # Initialize SubsManager with the user ID
        
        # Check if the user is still premium and if their subscription has expired
        is_premium_active = await self.check_premium_status()

        if not is_premium_active:
            btn_name_row1 = ["👑 Subscriptions Prices"]
            btn_data_row1 = ["query_subs_prices"]

            btn = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
            await Message.reply_msg(update, "You'r Subscrption is ended. Please renewal your subscription👑.", btn)
            QuizParameters.remove_mode(context)  # Disable quiz mode
            return False, 0

        # Check if the user has used all their coins for the selected program
        coins = 0
        
        if program == "p_quiz":
            coins = self.premium_quiz_coins
        elif program == "summary":
            coins = self.summary_coins
        elif program == "imagine":
            coins = self.imagine_coins
        elif program == "gpt":
            coins = self.gpt_coins
            
        # Fetch remaining premium quizzes (coins)
        remaining_coins = await self.get_remaining_coins()

        if remaining_coins < coins:
            btn_name_row1 = ["👑 Subscriptions Prices"]
            btn_data_row1 = ["query_subs_prices"]

            btn = await Button.cbutton(btn_name_row1, btn_data_row1, update= update)
            await Message.reply_msg(update, f"You don't have enough coins to use this {program}. Please buy more coins 🪙.", btn)
            QuizParameters.remove_mode(context)  # Disable quiz mode
            return False, remaining_coins
            

        # Selecte the mode based on the program
        if program == "p_quiz":
            QuizParameters.set_premium_quiz_mode(context)
        elif program == "summary":
            QuizParameters.set_summarize_mode(context)
        elif program == "imagine":
            QuizParameters.set_imagine_mode(context)
        elif program == "gpt":
            QuizParameters.set_gpt_mode(context)

        
            
        return True, remaining_coins
