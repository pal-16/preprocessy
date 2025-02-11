import numpy as np
import pandas as pd

from ..utils import num_of_samples


class Split:
    """Class for resampling and splitting input data

    Private Methods
    ---------------

    __validate__input() : validates input received by train_test_split()

    Public Methods
    --------------

    train_test_split() : Splits input data into train and test sets

    """

    def __init__(self):
        self.df = None
        self.X = None
        self.y = None
        self.test_size = None
        self.train_size = None
        self.random_state = 69

    def __validate_input(self):

        """Function to validate inputs received by train_test_split

        Parameters
        ----------

        X : pandas.core.frames.DataFrame
            Input dataframe, may or may not consist of the target label.

        y : pandas.core.series.Series
            Target label series. If None then X consists target label

        test_size : float or int
            Size of test set after splitting. Can take values from 0 - 1 for float point values,
            0 - Number of samples for integer values. Is complementary to train size.

        train_size : float or int
            Size of train set after splitting. Can take values from 0 - 1 for float point values,
            0 - Number of samples for integer values. Is complementary to test size.

        random_state : int
            Seeding to be provided for shuffling before splitting.

        Returns
        -------

        train_size: float or int
            Returns default value of 0.7 if not provided any value.

        test_size: float or int
            Returns default value of 0.3 if not provided any value.

        """

        if self.X is None:
            raise ValueError("Feature dataframe should not be of None")

        if not isinstance(self.X, pd.core.frame.DataFrame):
            raise TypeError(
                "Feature dataframe is not a valid dataframe.\nExpected object"
                " type: pandas.core.frame.DataFrame"
            )

        n_samples = num_of_samples(self.X)

        if self.y is not None:
            if n_samples != self.y.shape[0]:
                raise ValueError(
                    "Number of samples of target label and feature dataframe"
                    " unequal.\nSamples in feature dataframe:"
                    f" {self.X.shape[0]}\nSamples in target label: {self.y.shape[0]}"
                )
            if not isinstance(self.y, pd.core.series.Series):
                raise TypeError(
                    "Target label is not a valid dataframe.\nExpected object"
                    " type: pandas.core.series.Series"
                )
        if self.test_size and self.train_size:
            if not isinstance(self.test_size, int) or not isinstance(
                self.test_size, float
            ):
                raise TypeError("test_size must be of type int or float")
            if not isinstance(self.train_size, int) or not isinstance(
                self.train_size, float
            ):
                raise TypeError("train_size must be of type int or float")
            if not isinstance(self.test_size, self.train_size):
                raise TypeError(
                    "Data types of test_size and train_size do not"
                    f" match.\ntest_size: {type(self.test_size)}.\ntrain_size:"
                    f" {type(self.train_size)}"
                )
            if (
                isinstance(self.test_size, float)
                and self.test_size + self.train_size != 1
            ):
                raise ValueError("test_size + train_size should be equal to 1")
            elif (
                isinstance(self.test_size, int)
                and self.test_size + self.train_size != n_samples
            ):
                raise ValueError(
                    "test_size + train_size not equal to number of samples"
                )

        elif self.test_size:
            if isinstance(self.test_size, float) and (
                self.test_size < 0 or self.test_size > 1
            ):
                raise ValueError("test_size should be between 0 and 1")
            if isinstance(self.test_size, int) and (
                self.test_size < 0 or self.test_size > n_samples
            ):
                raise ValueError(
                    f"test_size should be between 0 and {n_samples}"
                )
            self.train_size = (
                1 - self.test_size
                if isinstance(self.test_size, float)
                else n_samples - self.test_size
            )

        elif self.train_size:
            if isinstance(self.train_size, float) and (
                self.train_size < 0 or self.train_size > 1
            ):
                raise ValueError("train_size should be between 0 and 1")
            if isinstance(self.train_size, int) and (
                self.train_size < 0 or self.train_size > n_samples
            ):
                raise ValueError(
                    f"train_size should be between 0 and {n_samples}"
                )
            self.test_size = (
                1 - self.train_size
                if isinstance(self.train_size, float)
                else n_samples - self.train_size
            )

        else:
            if self.y is None:
                self.test_size = 0.2
                self.train_size = 0.8
            else:
                features = len(self.X.columns)
                self.test_size = float(1 / np.sqrt(features))
                self.train_size = 1 - self.test_size

        if not isinstance(self.random_state, int):
            raise TypeError("random_state should be of type int")

    def train_test_split(self, params):
        """Performs train test split on the input data

        Parameters
        ----------
        X : pandas.core.frames.DataFrame
            Input dataframe, may or may not consist of the target label.
            Should not be None

        y : pandas.core.series.Series
            Target label series. If None then X consists target label

        test_size : float or int
            Size of test set after splitting. Can take values from 0 - 1 for float point values,
            0 - Number of samples for integer values. Is complementary to train size.

        train_size : float or int
            Size of train set after splitting. Can take values from 0 - 1 for float point values,
            0 - Number of samples for integer values. Is complementary to test size.

        random_state : int
            Seeding to be provided for shuffling before splitting.

        Returns
        -------

        If target label provided

            X_train : pandas.core.frames.DataFrame

            y_train : pandas.core.series.Series

            X_test : pandas.core.frames.DataFrame

            y_test : pandas.core.series.Series

        Else

            train : pandas.core.frames.DataFrame

            test : pandas.core.frames.DataFrame

        """

        if "X" in params.keys():
            self.X = params["X"]
        if "y" in params.keys():
            self.y = params["y"]
        if "test_size" in params.keys():
            self.test_size = params["test_size"]
        if "train_size" in params.keys():
            self.train_size = params["train_size"]
        if "random_state" in params.keys():
            self.random_state = params["random_state"]

        self.__validate_input()

        np.random.seed(self.random_state)

        if self.y is not None:
            self.df = pd.concat([self.X, self.y], axis=1)
        else:
            self.df = self.X

        self.df = self.df.iloc[
            np.random.permutation(len(self.df))
        ].reset_index(drop=True)
        if isinstance(self.test_size, float):
            index = int(self.test_size * len(self.df))
            train = self.df.iloc[index:]
            test = self.df.iloc[:index]
        else:
            train = self.df.iloc[self.test_size :]
            test = self.df.iloc[: self.test_size]

        if self.y is not None:
            if not self.y.name:
                raise ValueError(
                    f"Target column needs to have a name. ${self.y.name} was provided."
                )
            y_train = train[self.y.name]
            X_train = train.drop([self.y.name], axis=1)
            y_test = test[self.y.name]
            X_test = test.drop([self.y.name], axis=1)
            params["X_train"] = X_train
            params["X_test"] = X_test
            params["y_train"] = y_train
            params["y_test"] = y_test

        else:
            params["train"] = train
            params["test"] = test
