from itertools import chain

from ca.ascoderu.lokole.domain.email import EmailStore


class InMemoryEmailStore(EmailStore):
    def __init__(self, store=None):
        """
        :type store: list[dict] | None

        """
        self._store = store or []

    def inbox(self, email_address):
        return (dict(email) for email in self._store
                if email_address in email.get('to', []))

    def outbox(self, email_address):
        return (dict(email) for email in self._store
                if email_address == email.get('from')
                and email.get('sent_at') is None)

    def sent(self, email_address):
        return (dict(email) for email in self._store
                if email_address == email.get('from')
                and email.get('sent_at') is not None)

    def create(self, *emails):
        self._store.extend(map(dict, emails))

    def search(self, email_address, query):
        return (dict(email) for email in self._all_for(email_address)
                if query in email.get('subject')
                or query in email.get('body')
                or query in email.get('from')
                or any(query in to for to in email.get('to', [])))

    def pending(self):
        return (dict(email) for email in self._store
                if email.get('sent_at') is None)

    def _all_for(self, email_address):
        return chain(self.inbox(email_address),
                     self.outbox(email_address),
                     self.sent(email_address))