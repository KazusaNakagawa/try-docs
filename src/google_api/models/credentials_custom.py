import six

from google.auth import crypt
from google.oauth2.service_account import Credentials


class CredentialsCustom(Credentials):
    """ If json files cannot be handled, a hardcourt dictionary
    type is used to handle
    """

    @classmethod
    def from_service_account_file(cls, data, **kwargs):
        """Creates a Credentials instance from a service account json file.

        Args:
            data (dict): The path to the service account json file.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            google.auth.service_account.Credentials: The constructed
                credentials.
        """
        info, signer = cls.from_data(
            data, require=["client_email", "token_uri"]
        )
        return cls._from_signer_and_info(signer, info, **kwargs)
        pass

    @classmethod
    def from_data(cls, data, require=None, use_rsa_signer=True):
        """Reads a Google service account JSON file and returns its parsed info.

        Args:
            data (dict): key data
            require (Sequence[str]): List of keys required to be present in the
                info.
            use_rsa_signer (Optional[bool]): Whether to use RSA signer or EC signer.
                We use RSA signer by default.

        Returns:
            Tuple[ Mapping[str, str], google.auth.crypt.Signer ]: The verified
                info and a signer instance.
        """
        return data, cls.from_dict(data, require=require, use_rsa_signer=use_rsa_signer)

    @classmethod
    def from_dict(cls, data, require=None, use_rsa_signer=True):
        """Validates a dictionary containing Google service account data.

        Creates and returns a :class:`google.auth.crypt.Signer` instance from the
        private key specified in the data.

        Args:
            data (Mapping[str, str]): The service account data
            require (Sequence[str]): List of keys required to be present in the
                info.
            use_rsa_signer (Optional[bool]): Whether to use RSA signer or EC signer.
                We use RSA signer by default.

        Returns:
            google.auth.crypt.Signer: A signer created from the private key in the
                service account file.

        Raises:
            ValueError: if the data was in the wrong format, or if one of the
                required keys is missing.
        """
        keys_needed = set(require if require is not None else [])

        missing = keys_needed.difference(six.iterkeys(data))

        if missing:
            raise ValueError(
                "Service account info was not in the expected format, missing "
                "fields {}.".format(", ".join(missing))
            )

        # Create a signer.
        if use_rsa_signer:
            signer = crypt.RSASigner.from_service_account_info(data)
        else:
            signer = crypt.ES256Signer.from_service_account_info(data)

        return signer
